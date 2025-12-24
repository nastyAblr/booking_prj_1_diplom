from django import forms
from django.contrib.auth.forms import (UserCreationForm,
                                       UserChangeForm, AuthenticationForm)
from .models import CustomUser, CustomUserProfile


class CustomUserRegisterForm(UserCreationForm):  # форма регистрации пользователя с готовой встроенной логикой безопасности
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class CustomUserUpdateForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class CustomUserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(CustomUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class CustomUserProfileUpdateForm(forms.ModelForm): # форма профиля пользователя, может называться и так
    class Meta:
        model = CustomUserProfile
        fields = ('tagline',)

    def __init__(self, *args, **kwargs):
        super(CustomUserProfileUpdateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
