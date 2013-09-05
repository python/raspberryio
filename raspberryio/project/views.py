from django.http import HttpResponseForbidden, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required
from django.views.generic.list_detail import object_list
from django.core.cache import cache
from django.conf import settings

from actstream import action

from mezzanine.utils.sites import current_site_id
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED
from hilbert.decorators import ajax_only

from raspberryio.project.models import Project, ProjectStep, ProjectImage
from raspberryio.project.forms import (ProjectForm, ProjectStepForm,
    ProjectImageForm)
from raspberryio.project.utils import AjaxResponse, get_active_users


def index(request):
    "Custom view for site homepage"
    active_users = cache.get('active_users')
    if active_users is None:
        active_users = get_active_users(days=62, number=6)
        cache.set('active_users', active_users, 60 * 30)
    return render(request, 'homepage.html', {'active_users': active_users})


def project_list(request):
    "Show a list of published projects and order them by most recently created"
    projects = Project.objects.published(request.user).order_by('-created_datetime')
    return object_list(request, queryset=projects, paginate_by=12)


def project_detail(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)
    if not project.is_published(request):
        raise Http404('There is no project here')
    return render(request, 'project/project_detail.html', {
        'project': project,
        'DISQUS_SHORTNAME': settings.DISQUS_SHORTNAME,
        'DISQUS_HOSTNAME': settings.DISQUS_HOSTNAME,
    })


@login_required
def project_create_edit(request, project_slug=None):
    user = request.user
    site = Site.objects.get(id=current_site_id)
    if project_slug:
        project = get_object_or_404(Project, slug=project_slug)
    else:
        project = Project(user=user, site=site)
    if not project.is_editable(request):
        return HttpResponseForbidden('You are not the owner of this project.')
    project_form = ProjectForm(
        request.POST or None, request.FILES or None, instance=project
    )
    if project_form.is_valid():
        project_form.save()
        if project.is_published():
            action.send(user, verb='updated', target=project)
        if 'save-add-step' in request.POST:
            redirect_args = ('project-step-create-edit', project.slug)
        else:
            redirect_args = (project,)
        return redirect(*redirect_args)
    return render(request, 'project/project_create_edit.html', {
        'project': project,
        'project_form': project_form,
    })


@login_required
def project_step_create_edit(request, project_slug, project_step_number=None):
    user = request.user
    project = get_object_or_404(Project, slug=project_slug)
    if not project.is_editable(request):
        return HttpResponseForbidden('You are not the owner of this project.')
    if 'add' in request.path and project.steps.count() >= 20:
        messages.add_message(request, messages.WARNING,
                    'This project already contains 20 steps.')
        return redirect('project-detail', project.slug)
    if project_step_number is not None:
        project_step = get_object_or_404(
            ProjectStep, project=project, _order=project_step_number
        )
    else:
        project_step = ProjectStep(project=project)
    project_step_form = ProjectStepForm(
        request.POST or None, instance=project_step
    )
    if project_step_form.is_valid():
        project_step_form.save()
        if project.is_published():
            action.send(user, verb='updated', action_object=project_step, target=project)
        # User clicked "save and add another"
        if 'save-add' in request.POST:
            redirect_args = ('project-step-create-edit', project.slug)
        # User clicked "save" (catch anything else)
        else:
            redirect_args = (project,)
        return redirect(*redirect_args)
    return render(request, 'project/project_step_create_edit.html', {
        'project': project,
        'project_step': project_step,
        'project_step_form': project_step_form,
    })


@login_required
def project_delete(request, project_pk):
    project = get_object_or_404(Project, id=project_pk)
    if not project.is_editable(request):
        return HttpResponseForbidden('You are not the owner of this project.')
    if 'ok' in request.POST:
        project.delete()
        return redirect(request.user)
    return render(request, 'project/project_delete.html', {
        'project': project,
    })


@login_required
def project_step_delete(request, project_step_pk):
    project_step = get_object_or_404(ProjectStep, id=project_step_pk)
    if not project_step.is_editable(request):
        return HttpResponseForbidden('You are not the owner of this project.')
    if 'ok' in request.POST:
        project_step.delete()
        return redirect(project_step.project)
    return render(request, 'project/project_step_delete.html', {
        'project_step': project_step,
    })


@login_required
@ajax_only
def publish_project(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)
    if not project.is_editable(request):
        return HttpResponseForbidden('You are not the owner of this project.')
    else:
        project.status = CONTENT_STATUS_PUBLISHED
        project.save()
        action.send(request.user, verb='published', target=project)
    return AjaxResponse(request, {})


@login_required
@ajax_only
def gallery_image_create(request, project_slug=None, project_step_number=None):
    project_step = None
    if project_slug and project_step_number:
        project = get_object_or_404(Project, slug=project_slug)
        project_step = get_object_or_404(
            ProjectStep, project=project, _order=project_step_number
        )
        if not project.is_editable(request):
            return HttpResponseForbidden(
                'You are not the owner of this project.'
            )
    form = ProjectImageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        image = form.save()
        if project_step is not None:
            project_step.gallery.add(image)
        return AjaxResponse(request, ProjectImage.serialize(image))
    # A post was made without any files, just return False
    return AjaxResponse(request, False)


@login_required
@ajax_only
def gallery_image_download(request, project_slug, project_step_number):
    # Load and send thumbnails of existing files
    project = get_object_or_404(Project, slug=project_slug)
    project_step = get_object_or_404(
        ProjectStep, project=project, _order=project_step_number
    )
    images = project_step.gallery.all()
    return AjaxResponse(request, ProjectImage.serialize(images))


@login_required
@ajax_only
def gallery_image_delete(request, project_image_id):
    project_image = get_object_or_404(ProjectImage, id=project_image_id)
    try:
        project_step = project_image.projectstep_set.all()[0]
    except IndexError:
        # If the image doesn't belong to a project step, no need to check for
        # permission (and it isn't possible)
        pass
    else:
        if not project_step.is_editable(request):
            return HttpResponseForbidden('You are not the owner of this image.')
    # Remove the actual file, then the database record and return True
    project_image.file.delete()
    project_image.delete()
    return AjaxResponse(request, True)
