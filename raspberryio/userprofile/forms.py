from django import forms

from bootstrap_toolkit.widgets import BootstrapTextInput

from raspberryio.userprofile.models import Profile


class UserProfileForm(forms.ModelForm):
    # Custom fields
    twitter_id = forms.CharField(max_length=100,
        widget=BootstrapTextInput(prepend='@'),
    )

    class Meta:
        model = Profile
        fields = (
            'website', 'bio',  # Other fields
        )
