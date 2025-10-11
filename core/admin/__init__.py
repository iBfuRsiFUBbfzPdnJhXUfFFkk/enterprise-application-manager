from pathlib import Path

from core.admin.register_admin_models import register_admin_models

models_directory: Path = Path("core") / "models"
common_folder: Path = models_directory / "common"

register_admin_models(
    excludes=[
        common_folder,
    ],
    models_directory=models_directory,
)

# Import custom admin classes after automatic registration
# This allows custom admins to override the default BaseModelAdmin
from core.admin.role_admin import RoleAdmin  # noqa: E402, F401
