from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.conf import settings

from mezzanine.utils.sites import current_site_id
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED
from mezzanine.galleries.models import Gallery, GalleryImage
from hilbert.decorators import ajax_only
from hilbert.http import JsonResponse

from raspberryio.project.models import Project, ProjectStep
from raspberryio.project.forms import ProjectForm, ProjectStepForm


def project_list(request):
    user = request.user
    if user.is_superuser:
        projects = Project.objects.all()
    else:
        projects = Project.objects.published()
    return render(request, 'project/project_list.html', {
        'projects': projects,
    })


def project_detail(request, project_slug):
    user = request.user
    project = get_object_or_404(Project, slug=project_slug)
    if not project.is_published:
        if not user.is_superuser and project.user != user:
            raise Http404('There is no project here')
    return render(request, 'project/project_detail.html', {
        'project': project,
    })


@login_required
def project_create_edit(request, project_slug=None):
    user = request.user
    site = Site.objects.get(id=current_site_id)
    if project_slug:
        project = get_object_or_404(Project, slug=project_slug)
    else:
        project = Project(user=user, site=site)
    if project.user != user and not user.is_superuser:
        return HttpResponseForbidden('You are not the owner of this project.')
    project_form = ProjectForm(request.POST or None, instance=project)
    if project_form.is_valid():
        project_form.save()
        if not project.steps.exists():
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
    if project.user != user and not user.is_superuser:
        return HttpResponseForbidden('You are not the owner of this project.')
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
@ajax_only
def publish_project(request, project_slug):
    user = request.user
    project = get_object_or_404(Project, slug=project_slug)
    if user != project.user and user.is_superuser == False:
        return HttpResponseForbidden('You are not the owner of this project.')
    else:
        project.status = CONTENT_STATUS_PUBLISHED
        project.save()
    return JsonResponse({})


@login_required
@ajax_only
def publish_project(request, project_slug):
    user = request.user
    project = get_object_or_404(Project, slug=project_slug)
    if user != project.user and user.is_superuser == False:
        return HttpResponseForbidden('You are not the owner of this project.')
    else:
        project.status = CONTENT_STATUS_PUBLISHED
        project.save()
    return JsonResponse({})


class AjaxResponse(HttpResponse):
    """Like JsonResponse but uses text/plain for junky browsers"""

    def __init__(self, request, obj='', *args, **kwargs):
        content = simplejson.dumps(obj, {})
        mimetype = 'application/json' \
            if 'application/json' in request.META['HTTP_ACCEPT'] else 'text/plain'
        super(AjaxResponse, self).__init__(content, mimetype, *args, **kwargs)
        self['Content-Disposition'] = 'inline; filename=files.json'


@login_required
def gallery_image_create(request, project_slug, project_step_number):
    user = request.user
    project = get_object_or_404(Project, slug=project_slug)
    if project.user != user and not user.is_superuser:
        return HttpResponseForbidden('You are not the owner of this project.')
    project_step = get_object_or_404(
        ProjectStep, project=project, _order=project_step_number
    )
    if request.POST and 'file' in request.FILES:
        # FIXME: For the sake of all that's holy, use an actual form
        f = request.FILES.get('file')
        # Create a gallery for the project step if None exists, otherwise point to it
        if project_step.gallery:
            gallery = project_step.gallery
        else:
            gallery = Gallery.objects.create()
            project_step.gallery = gallery
            project_step.save()
        gallery_image = GalleryImage.objects.create(gallery=gallery, file=f)
        data = [{
            'name': f.name,
            'url': settings.MEDIA_URL + "pictures/" + f.name.replace(" ", "_"),
            'thumbnail_url': settings.MEDIA_URL + "pictures/" + f.name.replace(" ", "_"),
            'delete_url': reverse('delete-image', args=[gallery_image.id]),
            'delete_type': 'DELETE'
        }]
        return AjaxResponse(request, data)
    return AjaxResponse(request, False)


@login_required
def gallery_image_delete(request, gallery_image_id):
    user = request.user
    gallery_image = get_object_or_404(GalleryImage, id=gallery_image_id)
    if user != gallery_image.gallery.projectstep.project.user:
        return HttpResponseForbidden('You are not the owner of this project.')
    else:
        gallery_image.delete()
        return AjaxResponse(request, True)
