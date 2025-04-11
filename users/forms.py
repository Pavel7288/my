from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.forms import CharField

from users.models import User


class UserLoginForm(AuthenticationForm):
    # username = forms.CharField()
    # password = forms.CharField()
    class Meta:
        model = User
        # fields = ('username', 'password') хз зачем это, и без него работает


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            # "first_name",
            # "last_name",
            'number',
            'username',
            "email",
            "password1",
            "password2",
        )
        # first_name = forms.CharField(
        #     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя'}),
        # )
        # last_name = forms.CharField(
        #     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите фамилию'}),
        # )
        # username = forms.CharField(
        #     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя'}),
        # )
        # email = forms.CharField(
        #     widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите email'}),
        # )
        # password1 = forms.CharField(
        #     widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}),
        # )
        # password2 = forms.CharField(
        #     widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтвердите пароль'}),
        # )


class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'number',
            'username',
            "email")
        number = CharField()
        username = CharField()
        email = CharField()