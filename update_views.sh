#!/bin/bash

# Update dependency views
cat > core/views/dependency/dependency_add_view.py << 'PYTHON'
from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.dependency_form import DependencyForm
from core.utilities.base_render import base_render


def dependency_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = DependencyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='dependency')
    else:
        form = DependencyForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/dependency/dependency_form.html'
    )
PYTHON

cat > core/views/dependency/dependency_edit_view.py << 'PYTHON'
from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.dependency_form import DependencyForm
from core.models.dependency import Dependency
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def dependency_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        dependency = Dependency.objects.get(id=model_id)
    except Dependency.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = DependencyForm(request.POST, instance=dependency)
        if form.is_valid():
            form.save()
            return redirect(to='dependency')
    else:
        form = DependencyForm(instance=dependency)

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/dependency/dependency_form.html'
    )
PYTHON

# Update database views
cat > core/views/database/database_add_view.py << 'PYTHON'
from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.database_form import DatabaseForm
from core.utilities.base_render import base_render


def database_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = DatabaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='database')
    else:
        form = DatabaseForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/database/database_form.html'
    )
PYTHON

cat > core/views/database/database_edit_view.py << 'PYTHON'
from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.database_form import DatabaseForm
from core.models.database import Database
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def database_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        database = Database.objects.get(id=model_id)
    except Database.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = DatabaseForm(request.POST, instance=database)
        if form.is_valid():
            form.save()
            return redirect(to='database')
    else:
        form = DatabaseForm(instance=database)

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/database/database_form.html'
    )
PYTHON

# Update document views
cat > core/views/document/document_add_view.py << 'PYTHON'
from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.document_form import DocumentForm
from core.utilities.base_render import base_render


def document_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='document')
    else:
        form = DocumentForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/document/document_form.html'
    )
PYTHON

cat > core/views/document/document_edit_view.py << 'PYTHON'
from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.document_form import DocumentForm
from core.models.document import Document
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def document_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        document = Document.objects.get(id=model_id)
    except Document.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = DocumentForm(request.POST, instance=document)
        if form.is_valid():
            form.save()
            return redirect(to='document')
    else:
        form = DocumentForm(instance=document)

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/document/document_form.html'
    )
PYTHON

# Update secret views
cat > core/views/secret/secret_add_view.py << 'PYTHON'
from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.secret_form import SecretForm
from core.utilities.base_render import base_render


def secret_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = SecretForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='secret')
    else:
        form = SecretForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/secret/secret_form.html'
    )
PYTHON

cat > core/views/secret/secret_edit_view.py << 'PYTHON'
from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.secret_form import SecretForm
from core.models.secret import Secret
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def secret_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        secret = Secret.objects.get(id=model_id)
    except Secret.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = SecretForm(request.POST, instance=secret)
        if form.is_valid():
            form.save()
            return redirect(to='secret')
    else:
        form = SecretForm(instance=secret)

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/secret/secret_form.html'
    )
PYTHON

echo "All views updated successfully!"
