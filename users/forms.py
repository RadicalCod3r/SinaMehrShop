from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User

class UserAdminAddForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords dont match')

        return password2

    def save(self, commit=True):
        user = super(UserAdminAddForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        
        if commit:
            user.save()

        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('phone', 'email', 'password', 'name', 'image', 'is_staff', 'is_superuser', 'is_active', 'logged_in')

    def clean_password(self):
        return self.initial['password']