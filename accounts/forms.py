from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
# from django_recaptcha.fields import ReCaptchaField
from .models import User, OTP


class UserCreationForm(forms.ModelForm):
    """
    Custom user creation form.
    """
    # capcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    User edit form.
    """
    password = ReadOnlyPasswordHashField(help_text=
                                         "You Can Change The Password Using <a href=\"../password/\">This Form</a>.")

    class Meta:
        model = User
        fields = '__all__'


class OTPForm(forms.Form):
    code = forms.CharField(max_length=5)

    def clean_code(self):
        code = self.cleaned_data['code']
        if not code.isdigit() or len(code) != 5:
            raise forms.ValidationError('Enter 5 digits only')

        try:
            OTP.objects.get(code=code)
        except OTP.DoesNotExist:
            raise forms.ValidationError('kolan hamchin codi mojod nist')

        return code


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', )
