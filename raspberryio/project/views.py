from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required
from django.utils import simplejson

from mezzanine.utils.sites import current_site_id
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED
from hilbert.decorators import ajax_only

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
    project = get_object_or_404(Project, slug=project_slug)
    if request.user != project.user:
        return HttpResponseForbidden('You are not the owner of this project.')
    else:
        project.status = CONTENT_STATUS_PUBLISHED
        project.save()
    json = simplejson.dumps({})
    return HttpResponse(json, mimetype='application/json')
