from django.contrib.auth import login
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.feature_flags import FEATURE_REMEMBER_ME_LOGIN
from core.forms.login_form import LoginForm
from core.utilities.base_render import base_render


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user: AbstractBaseUser = form.get_user()
            login(request=request, user=user)

            # Session always expires when browser closes
            request.session.set_expiry(0)

            return redirect(to='/authenticated/home/')
    else:
        form = LoginForm()

    return base_render(
        context={
            'form': form,
            'feature_remember_me': FEATURE_REMEMBER_ME_LOGIN,
        },
        request=request,
        template_name='login/login.html',
    )
