from pathlib import Path

from core.admin.register_admin_models import register_admin_models

# Import custom admin classes BEFORE automatic registration
# This ensures they are registered first, and automatic registration will skip them
from core.admin.role_admin import RoleAdmin  # noqa: E402, F401
from core.admin.estimation_item_admin import EstimationItemAdmin  # noqa: E402, F401

models_directory: Path = Path("core") / "models"
common_folder: Path = models_directory / "common"

register_admin_models(
    excludes=[
        common_folder,
    ],
    models_directory=models_directory,
)
