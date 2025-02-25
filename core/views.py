from os import getenv
from typing import Mapping, Any

from django.db.models import Model
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from core.forms import ApplicationForm, PersonForm
from core.models import Application, Person


# HOME
def home_view(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name="home.html")


# APPLICATION
def application_view(request: HttpRequest) -> HttpResponse:
    applications: QuerySet = Application.objects.all().order_by('-id')
    context: Mapping[str, Any] = {'applications': applications}
    return render(context=context, request=request, template_name="application.html")

def application_edit_view(request: HttpRequest, application_id: int) -> HttpResponse:
    application: Application = Application.objects.get(id=application_id)
    if request.method == 'POST':
        form: ApplicationForm[Model] = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return redirect('application')
    else:
        form: ApplicationForm[Model] = ApplicationForm(instance=application)
    context: Mapping[str, Any] = {'form': form}
    return render(context=context, request=request, template_name='application_edit.html')


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
    people: QuerySet = Person.objects.all().order_by('name_last', 'name_first', 'id')
    hostname_gitlab: str = getenv('HOSTNAME_GITLAB') or "gitlab.com"
    context: Mapping[str, Any] = {'hostname_gitlab': hostname_gitlab, 'people': people}
    return render(context=context, request=request, template_name="person.html")

def person_edit_view(request: HttpRequest, person_id: int) -> HttpResponse:
    person: Person = Person.objects.get(id=person_id)
    if request.method == 'POST':
        form: PersonForm[Model] = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('person')
    else:
        form: PersonForm[Model] = PersonForm(instance=person)
    context: Mapping[str, Any] = {'form': form}
    return render(context=context, request=request, template_name='person_edit.html')

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
