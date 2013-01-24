from django.contrib import admin
from raspberryio.project import models as project
from raspberryio.project.forms import ProjectForm


class ProjectAdmin(admin.ModelAdmin):
    model = project.Project
    form = ProjectForm
    list_display = ('title', 'created_datetime', 'admin_thumb')

admin.site.register(project.Project, ProjectAdmin)
