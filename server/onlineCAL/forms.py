from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm)


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = ''
        self.fields['username'].widget.attrs['placeholder'] = 'Email ID'

        self.fields['password'].label = ''
        self.fields['password'].widget.attrs['placeholder'] = 'Password'


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].label = ''
        self.fields['email'].widget.attrs['placeholder'] = 'Email ID'


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['new_password1'].label = ''
        self.fields['new_password1'].widget.attrs['placeholder'] = 'New Password'

        self.fields['new_password2'].label = ''
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
