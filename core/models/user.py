from simple_history.models import HistoricalRecords

from django.contrib.auth.models import AbstractUser
from core.models.common.abstract.comment import Comment
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar


class User(AbstractUser, Comment):
    history = HistoricalRecords(excluded_fields=['history_user'])
    ldap_field = create_generic_varchar()
