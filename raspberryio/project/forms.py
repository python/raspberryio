from django import forms
from raspberryio.project.models import Project, ProjectStep


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = (
            'title', 'featured_photo', 'featured_video', 'tldr', 'categories',
            'status', 'publish_date',
        )


class ProjectStepForm(forms.ModelForm):

    class Meta:
        model = ProjectStep
        fields = (
            'content', 'gallery', 'video'
        )
