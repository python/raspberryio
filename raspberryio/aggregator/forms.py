from __future__ import absolute_import

from django import forms
from .models import Feed


class FeedModelForm(forms.ModelForm):
    title = forms.CharField(max_length=250,
                            help_text="Please enter the title of your blog.")
    feed_url = forms.URLField(label='Feed URL',
                              help_text="Link to RSS/Atom feed. Please use only Raspberry Pi related feeds.")
    public_url = forms.URLField(label='Public URL',
                                help_text="Link to the homepage for your blog.")

    class Meta:
        model = Feed
        exclude = ('is_defunct', 'feed_type', 'owner', 'approval_status')
