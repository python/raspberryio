from django import forms
from django.contrib import admin

from raspberryio.project.models import Project, ProjectStep, ProjectCategory
from mezzanine.blog.models import BlogCategory


class ProjectAdminForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = (
            'title', 'status', 'publish_date', 'user', 'featured_photo',
            'featured_video', 'tldr', 'categories'
        )


class ProjectStepInline(admin.TabularInline):
    model = ProjectStep
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    model = Project
    form = ProjectAdminForm
    list_display = ('title', 'created_datetime', 'admin_thumb')
    inlines = (ProjectStepInline,)
    raw_id_fields = ('user',)


class ProjectCategoryAdmin(admin.ModelAdmin):
    model = ProjectCategory
    fields = ('title',)

admin.site.register(Project, ProjectAdmin)
#try:
#    admin.site.unregister(BlogCategory)
#except:
#    pass
admin.site.register(ProjectCategory, ProjectCategoryAdmin)
