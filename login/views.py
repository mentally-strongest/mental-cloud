from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from login.forms import LogInForm, SignUpForm
from login.models import User

class LogInView(LoginView):
    template_name = 'login/login.html'
    form_class = LogInForm
    model = User

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')

        next_page = request.GET.get('next') or 'home'
        form = LogInForm()
        return render(request, self.template_name, {'form': form, 'next': next_page})


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'login/signup.html'

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            return render(request, self.template_name, {'form': form})

