from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label='Подтвердите пароль',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', )
        widgets = {
            'username': forms.TextInput(attrs={'autofocus': True}),
        }
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }

        help_texts = {
            'username': None,
        }


    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2',
            Submit('submit', 'Зарегистрироваться', css_class="btn btn-primary btn-lg btn-block")
        )


class LoginForm(AuthenticationForm):
        username = UsernameField(
            label='Логин',
            widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': True, 'required': True})
        )
        password = forms.CharField(
            label='Пароль',
            widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': True})
        )

