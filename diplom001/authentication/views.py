from django.contrib.auth.views import LogoutView, LoginView
from django.shortcuts import redirect
from django.views.generic import CreateView

from authentication.forms import RegisterForm
from authentication.models import User


class Login(LoginView):
    http_method_names = ['get', 'post']
    redirect_authenticated_user = True
    template_name = 'authentication/login.html'


class Logout(LogoutView):
    next_page = '/'
    http_method_names = ['get']
    template_name = 'authentication/logout.html'

    def get(self, *args, **kwargs):
        super().get(*args, **kwargs)
        return redirect('list')


class Register(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'authentication/register.html'
    success_url = '/'
