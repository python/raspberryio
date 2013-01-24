from django.shortcuts import render, get_object_or_404

from raspberryio.project.models import Project


def project_list(request):
    projects = Project.objects.published()
    return render(request, 'project/project_list.html', {
        'projects': projects,
    })


def project_detail(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)
    return render(request, 'project/project_detail.html', {
        'project': project,
    })
