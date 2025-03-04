from importlib import import_module
from inspect import getmembers, isclass
from os import walk
from os.path import relpath, join, sep
from pathlib import Path
from types import ModuleType

from django.db.models import Model

from core.admin.should_skip_admin_directory import should_skip_admin_directory


def get_admin_model_classes(
        excludes: list[Path] | None = None,
        models_directory: Path | None = None,
) -> list[type[Model]]:
    models_directory_str: str = str(models_directory)
    if excludes is None:
        excludes = []
    exclude_strings: list[str] = [str(exclude) for exclude in excludes]
    model_classes: list[type[Model]] = []
    for root, _, files in walk(top=models_directory):
        if should_skip_admin_directory(
                exclude_strings=exclude_strings,
                root_directory=root
        ):
            continue

        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                module_name: str = relpath(path=join(root, file), start=models_directory_str).replace(sep, ".")[:-3]
                module: ModuleType = import_module(f"{models_directory_str.replace(sep, '.')}.{module_name}")

                for name, obj in getmembers(module):
                    if isclass(object=obj):
                        if hasattr(obj, 'objects') and hasattr(obj, '_meta'):
                            model_classes.append(obj)
    return model_classes
