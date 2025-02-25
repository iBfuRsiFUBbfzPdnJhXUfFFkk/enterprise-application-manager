from os import getenv
from typing import Mapping, Any

from django.db.models import Model
from django.db.models.query import QuerySet
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from core.forms import ApplicationForm, PersonForm, DatabaseForm
from core.models import Application, Person, Database


def generic_add_view(
        form_cls: type[ModelForm],
        request: HttpRequest,
        success_route: str,
) -> HttpResponse:
    method: str | None = request.method
    immutable_query_dict = request.POST
    if method == 'POST':
        form: ModelForm[Model] = form_cls(immutable_query_dict)
        if form.is_valid():
            form.save()
            return redirect(to=success_route)
    else:
        form: ModelForm[Model] = form_cls()
    context: Mapping[str, Any] = {'form': form}
    return render(context=context, request=request, template_name='generic_add.html')


def generic_edit_view(
        form_cls: type[ModelForm],
        model_cls: type[Model],
        model_id: int,
        request: HttpRequest,
        success_route: str,
) -> HttpResponse:
    method: str | None = request.method
    immutable_query_dict = request.POST
    model_instance: Model = model_cls.objects.get(id=model_id)
    if method == 'POST':
        form: ModelForm = form_cls(immutable_query_dict, instance=model_instance)
        if form.is_valid():
            form.save()
            return redirect(to=success_route)
    else:
        form: ModelForm = form_cls(instance=model_instance)
    context: Mapping[str, Any] = {'form': form}
    return render(context=context, request=request, template_name='generic_edit.html')


def generic_view(
        context_name: str,
        field_names: list[str],
        model_cls: type[Model],
        request: HttpRequest,
        template_name: str,
        additional_context: Mapping[str, Any] | None = None,
) -> HttpResponse:
    models: QuerySet = model_cls.objects.all().order_by(*field_names)
    additional_context: Mapping[str, Any] = additional_context or {}
    context: Mapping[str, Any] = {**additional_context, context_name: models}
    return render(context=context, request=request, template_name=template_name)


# HOME
def home_view(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name="home.html")


# APPLICATION
def application_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        context_name="applications",
        field_names=['application_name', '-id'],
        model_cls=Application,
        request=request,
        template_name='application.html',
    )


def application_edit_view(request: HttpRequest, application_id: int) -> HttpResponse:
    return generic_edit_view(
        form_cls=ApplicationForm,
        model_cls=Application,
        model_id=application_id,
        request=request,
        success_route='application',
    )


def application_add_view(request: HttpRequest) -> HttpResponse:
    return generic_add_view(
        form_cls=ApplicationForm,
        request=request,
        success_route='application',
    )


# PERSON
def person_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        context_name="people",
        field_names=['name_last', 'name_first', 'id'],
        model_cls=Person,
        request=request,
        template_name='person.html',
        additional_context={'hostname_gitlab': getenv('HOSTNAME_GITLAB') or "gitlab.com"},
    )


def person_edit_view(request: HttpRequest, person_id: int) -> HttpResponse:
    return generic_edit_view(
        form_cls=PersonForm,
        model_cls=Person,
        model_id=person_id,
        request=request,
        success_route='person',
    )


def person_add_view(request: HttpRequest) -> HttpResponse:
    return generic_add_view(
        form_cls=PersonForm,
        request=request,
        success_route='person',
    )


# DATABASE
def database_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        context_name="databases",
        field_names=['database_name', '-id'],
        model_cls=Database,
        request=request,
        template_name='database.html',
    )


def database_edit_view(request: HttpRequest, database_id: int) -> HttpResponse:
    return generic_edit_view(
        form_cls=DatabaseForm,
        model_cls=Database,
        model_id=database_id,
        request=request,
        success_route='database',
    )


def database_add_view(request: HttpRequest) -> HttpResponse:
    return generic_add_view(
        form_cls=DatabaseForm,
        request=request,
        success_route='database',
    )
