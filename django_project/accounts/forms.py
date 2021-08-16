from django import forms
import re

from django.conf import settings
from django.core.exceptions import ValidationError

from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'avatar']

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        match = re.fullmatch(settings.NICKNAME_REGEX, nickname)
        if not match:
            raise ValidationError('Nickname contains invalid characters')
        return nickname