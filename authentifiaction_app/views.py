from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from authentifiaction_app.forms import RegisterForm, LoginForm



class SignupView(CreateView):
    form_class = RegisterForm
    success_url = '/'
    template_name = 'authentifiaction_app/register.html'


class UserLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'authentifiaction_app/login.html'
    authentication_form = LoginForm
