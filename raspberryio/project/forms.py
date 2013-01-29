from django import forms
from raspberryio.project.models import Project


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = (
            'title', 'status', 'publish_date', 'featured_photo',
            'featured_video', 'tldr', 'categories'
        )
