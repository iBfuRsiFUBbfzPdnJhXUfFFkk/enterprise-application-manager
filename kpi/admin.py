from pathlib import Path

from core.admin import register_admin_models

models_directory: Path = Path("kpi") / "models"

register_admin_models(
    excludes=[],
    models_directory=models_directory,
)
