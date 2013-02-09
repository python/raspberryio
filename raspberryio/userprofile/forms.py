from mezzanine.accounts.forms import ProfileForm
from bootstrap_toolkit.widgets import BootstrapTextInput


class PlaceHolderMixin(object):
    """
    Mixin that sets text input placeholder's to their label's value and removes
    the label.
    """
    def __init__(self, *args, **kwargs):
        super(PlaceHolderMixin, self).__init__(*args, **kwargs)
        for name, field in self.fields.iteritems():
            is_textarea = 'cols' in field.widget.attrs
            if hasattr(field.widget, 'input_type') or is_textarea:
                placeholder = field.label if field.label else name
                placeholder = placeholder.replace('_', ' ')
                field.widget.attrs.update({'placeholder': placeholder.title()})
                field.label = ''


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
