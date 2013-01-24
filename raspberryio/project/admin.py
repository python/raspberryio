from django.contrib import admin
from raspberryio.project.models import Project, ProjectStep
from raspberryio.project.forms import ProjectForm


class ProjectStepInline(admin.TabularInline):
    model = ProjectStep
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    model = Project
    form = ProjectForm
    list_display = ('title', 'created_datetime', 'admin_thumb')
    inlines = (ProjectStepInline,)
    raw_id_fields = ('user',)

admin.site.register(Project, ProjectAdmin)
