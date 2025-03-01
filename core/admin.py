from importlib import import_module
from inspect import getmembers, isclass
from os import walk
from os.path import relpath, join, sep
from types import ModuleType

from django.contrib import admin
from django.db.models import Model
from simple_history.admin import SimpleHistoryAdmin

models_directory = "core/models"
common_folder = f"{models_directory}/common"


def get_model_classes() -> list[type[Model]]:
    model_classes: list[type[Model]] = []
    for root, _, files in walk(top=models_directory):
        if common_folder in root:
            continue  # skip the model in common

        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                module_name: str = relpath(path=join(root, file), start=models_directory).replace(sep, ".")[:-3]
                module: ModuleType = import_module(f"{models_directory.replace(sep, '.')}.{module_name}")

                for name, obj in getmembers(module):
                    if isclass(object=obj):
                        if hasattr(obj, 'objects') and hasattr(obj, '_meta'):
                            model_classes.append(obj)
    return model_classes


def register_models():
    model_classes: list[type[Model]] = get_model_classes()
    for model_class in model_classes:
        if model_class in admin.site._registry:
            continue  # skip if already registered
        try:
            admin.site.register(
                admin_class=SimpleHistoryAdmin,
                model_or_iterable=model_class,
            )
        except Exception as error:
            print(f"Error registering {model_class.__name__}: {error}")


register_models()
