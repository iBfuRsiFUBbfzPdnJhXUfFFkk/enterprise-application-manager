from django.contrib.auth import login
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm

def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user: AbstractBaseUser = form.get_user()
            login(request=request, user=user)
            return redirect(to='/authenticated/home/')
    else:
        form = AuthenticationForm()
    return render(
        context={'form': form},
        request=request,
        template_name='login/login.html',
    )
