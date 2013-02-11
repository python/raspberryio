from gdata.youtube.service import YouTubeService as yt_service

from django import forms

from raspberryio.project.models import Project, ProjectStep, ProjectImage
from raspberryio.project.utils import get_youtube_video_id


PLACEHOLDER_WIDGET_TYPES = (
    'TextInput', 'PasswordInput', 'Textarea',
)


class PlaceHolderMixin(object):
    """
    Mixin that sets the placeholders of fields to their label's value and removes
    the label.
    """
    def __init__(self, *args, **kwargs):
        super(PlaceHolderMixin, self).__init__(*args, **kwargs)
        for name, field in self.fields.iteritems():
            widget_type = field.widget.__class__.__name__
            if widget_type in PLACEHOLDER_WIDGET_TYPES:
                placeholder = field.label if field.label else name
                placeholder = placeholder.replace('_', ' ')
                field.widget.attrs.update({'placeholder': placeholder.title()})
                field.label = ''


class ProjectForm(PlaceHolderMixin, forms.ModelForm):

    class Meta(object):
        model = Project
        fields = (
            'title', 'featured_photo', 'featured_video', 'tldr', 'categories',
        )

    def clean_featured_video(self):
        data = self.cleaned_data.get('featured_video', '')
        if data:
            video_id = get_youtube_video_id(data)
            try:
                yt_service().GetYouTubeVideoEntry(video_id=video_id)
            except:
                msg = "The supplied URL is not a valid Youtube video"
                raise forms.ValidationError(msg)
        return data


class ProjectStepForm(PlaceHolderMixin, forms.ModelForm):

    images = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean_images(self):
        images_str = self.cleaned_data.get('images', '')
        image_pks = images_str.split(',') if images_str else []
        try:
            image_pks = [int(pk) for pk in image_pks]
        except ValueError:
            image_pks = []
        self.images = image_pks

    def clean_video(self):
        data = self.cleaned_data.get('video', '')
        if data:
            video_id = get_youtube_video_id(data)
            try:
                yt_service().GetYouTubeVideoEntry(video_id=video_id)
            except:
                msg = "The supplied URL is not a valid Youtube video"
                raise forms.ValidationError(msg)
        return data

    def save(self, *args, **kwargs):
        result = super(ProjectStepForm, self).save(*args, **kwargs)
        if self.images:
            self.instance.gallery.add(*self.images)
        return result

    class Meta(object):
        model = ProjectStep
        fields = (
            'content', 'video', 'images'
        )


class ProjectImageForm(forms.ModelForm):

    def clean(self):
        files_data = self.files.get('file', None)
        if not files_data:
            raise forms.ValidationError('No file data present')
        self.data['file'] = files_data

    def save(self):
        file_data = self.data['file']
        instance = self.instance
        if file_data:
            instance.file = file_data
            instance.save()
        return instance

    class Meta(object):
        model = ProjectImage
