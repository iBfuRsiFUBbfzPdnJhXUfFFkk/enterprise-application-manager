from core.models.common.abstract.comment import Comment
from core.models.common.field_factories.create_generic_date import create_generic_date
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar


class ReleaseBundle(Comment):
    bundle_name = create_generic_varchar()
    date_code_freeze = create_generic_date()
    date_demo = create_generic_date()
    date_release = create_generic_date()

    def __str__(self):
        return f"{self.bundle_name}"
