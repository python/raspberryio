from django import forms
from raspberryio.project.models import Project, ProjectStep


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = (
            'title', 'featured_photo', 'featured_video', 'tldr', 'categories',
        )


class ProjectStepForm(forms.ModelForm):

    images = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean_images(self):
        images_str = self.cleaned_data.get('images', '')
        image_pks = images_str.split(',') if images_str else []
        try:
            image_pks = [int(pk) for pk in image_pks]
        except ValueError:
            image_pks = []
        else:
            self.images = image_pks

    def save(self, *args, **kwargs):
        result = super(ProjectStepForm, self).save(*args, **kwargs)
        if self.images:
            self.instance.gallery.add(*self.images)
        return result

    class Meta:
        model = ProjectStep
        fields = (
            'content', 'video', 'images'
        )
