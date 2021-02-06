from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.password_validation import password_validators_help_texts
from django.template.loader import render_to_string


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].label = ''
        self.fields['email'].widget.attrs['placeholder'] = 'Email ID'


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        context = {
            'help_texts': password_validators_help_texts(),
        }
        help_text = render_to_string(
            'registration/password_validation_help_text.html',
            context,
        )

        self.fields['new_password1'].label = ''
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Enter Password'
        self.fields['new_password1'].help_text = help_text

        self.fields['new_password2'].label = ''
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
