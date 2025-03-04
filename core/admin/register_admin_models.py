from pathlib import Path

from django.contrib import admin
from django.db.models import Model

from core.admin.base_model_admin import BaseModelAdmin
from core.admin.get_admin_model_classes import get_admin_model_classes


def register_admin_models(
        excludes: list[Path] | None = None,
        models_directory: Path | None = None,
):
    model_classes: list[type[Model]] = get_admin_model_classes(
        excludes=excludes,
        models_directory=models_directory,
    )
    for model_class in model_classes:
        if model_class in admin.site._registry:
            continue
        try:
            admin.site.register(
                admin_class=BaseModelAdmin,
                model_or_iterable=model_class,
            )
        except Exception as error:
            print(f"Error registering {model_class.__name__}: {error}")
