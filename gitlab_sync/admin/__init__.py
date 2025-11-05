from pathlib import Path

from core.admin.register_admin_models import register_admin_models

models_directory: Path = Path("gitlab_sync") / "models"
common_folder: Path = models_directory / "common"

register_admin_models(
    excludes=[
        common_folder,
    ],
    models_directory=models_directory,
)
