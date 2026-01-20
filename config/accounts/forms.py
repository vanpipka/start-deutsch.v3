from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={
            "class": "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring",
            "placeholder": "Введите логин"
        })
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            "class": "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring",
            "placeholder": "Введите пароль"
        })
    )


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            "class": "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring"
        })
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(attrs={
            "class": "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring"
        })
    )

    class Meta:
        model = User
        fields = ("username", "email")
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring"
            }),
            "email": forms.EmailInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring"
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise ValidationError("Пароли не совпадают")
        return cleaned_data
