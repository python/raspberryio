from gdata.youtube.service import YouTubeService as yt_service

from django import forms

from raspberryio.project.models import Project, ProjectStep
from raspberryio.project.utils import get_youtube_video_id


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = (
            'title', 'featured_photo', 'featured_video', 'tldr', 'categories',
        )

    def clean_featured_video(self):
        url = self.cleaned_data['featured_video']
        video_id = get_youtube_video_id(url)
        try:
            yt_service().GetYouTubeVideoEntry(video_id=video_id)
        except:
            msg = "The supplied URL is not a valid Youtube video"
            raise forms.ValidationError(msg)


class ProjectStepForm(forms.ModelForm):

    class Meta:
        model = ProjectStep
        fields = (
            'content', 'gallery', 'video'
        )

    def clean_video(self):
        url = self.cleaned_data['video']
        video_id = get_youtube_video_id(url)
        try:
            yt_service().GetYouTubeVideoEntry(video_id=video_id)
        except:
            msg = "The supplied URL is not a valid Youtube video"
            raise forms.ValidationError(msg)
