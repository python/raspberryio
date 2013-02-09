from mezzanine.accounts.forms import ProfileForm
from bootstrap_toolkit.widgets import BootstrapTextInput

from raspberryio.project.forms import PlaceHolderMixin


class UserProfileForm(PlaceHolderMixin, ProfileForm):

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        twitter_id_field = self.fields['twitter_id']
        twitter_id_field.widget = BootstrapTextInput(
            prepend='@',
        )
        twitter_id_field.widget.attrs.update({
            'placeholder': 'Twitter Id'
        })
