from mezzanine.accounts.forms import ProfileForm
from bootstrap_toolkit.widgets import BootstrapTextInput


class UserProfileForm(ProfileForm):

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['twitter_id'].widget = BootstrapTextInput(prepend='@')
