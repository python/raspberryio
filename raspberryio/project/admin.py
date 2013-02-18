import Image

from django import forms
from django.contrib import admin

from raspberryio.project.models import (FeaturedProject, Project, ProjectStep,
    ProjectCategory)


class FeaturedProjectAdminForm(forms.ModelForm):

    class Meta:
        model = FeaturedProject

    def clean_photo(self):
        photo = self.cleaned_data.get('photo', False)
        if 'photo' in self.changed_data:
            img = Image.open(photo)
            if photo.size > 5 * 1024 * 1024:
                error = "Photo file too large ( maximum 5MB )"
                raise forms.ValidationError(error)
            if img.size[0] < 1252 or img.size[1] < 626:
                error = "Photo dimensions too small ( minimum 1252x636 pixels )"
                raise forms.ValidationError(error)
        return photo


class FeaturedProjectAdmin(admin.ModelAdmin):
    model = FeaturedProject
    form = FeaturedProjectAdminForm
    list_display = ('project', 'featured_start_date')


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

admin.site.register(FeaturedProject, FeaturedProjectAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectCategory, ProjectCategoryAdmin)
