from typing import Mapping, Any

from django.db.models import Model
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from core.forms import ApplicationForm, PersonForm
from core.models import Application


# HOME
def home_view(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name="home.html")


# APPLICATION
def application_view(request: HttpRequest) -> HttpResponse:
    applications: QuerySet = Application.objects.all().order_by('-id')
    context: Mapping[str, Any] = {'applications': applications}
    return render(context=context, request=request, template_name="application.html")


def application_add_view(request: HttpRequest) -> HttpResponse:
    method: str | None = request.method
    if method == 'POST':
        form: ApplicationForm[Model] = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('application_added')
    else:
        form: ApplicationForm[Model] = ApplicationForm()
    context: Mapping[str, Any] = {'form': form}
    return render(context=context, request=request, template_name='application_add.html')


def application_added_view(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name='application_added.html')


# PERSON
def person_view(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name="person.html")


def person_add_view(request: HttpRequest) -> HttpResponse:
    method: str | None = request.method
    if method == 'POST':
        form: PersonForm[Model] = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='person_added')
    else:
        form: PersonForm[Model] = PersonForm()
    context: Mapping[str, Any] = {'form': form}
    return render(context=context, request=request, template_name='person_add.html')


def person_added_view(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name='person_added.html')
