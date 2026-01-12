from django.contrib.auth.models import AbstractUser
from django.db import models
from simple_history.models import HistoricalRecords

from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_enumeration_attack_uuid import AbstractEnumerationAttackUuid
from core.models.common.enums.bookmark_view_preference_choices import (
    BOOKMARK_VIEW_CARD,
    BOOKMARK_VIEW_PREFERENCE_CHOICES,
)
from core.models.person import Person

class User(
    AbstractComment,
    AbstractEnumerationAttackUuid,
    AbstractUser,
):
    active_directory_globally_unique_identifier_guid: str | None = models.CharField(max_length=255, null=True, blank=True)
    active_directory_security_accounts_manager_account_name: str | None = models.CharField(max_length=255, null=True, blank=True)
    active_directory_security_accounts_manager_account_type: str | None = models.CharField(max_length=255, null=True, blank=True)
    active_directory_security_identifier_sid: str | None = models.CharField(max_length=255, null=True, blank=True)
    bookmark_view_preference: str = models.CharField(
        max_length=255,
        choices=BOOKMARK_VIEW_PREFERENCE_CHOICES,
        null=True,
        blank=True
    )
    employee_company: str | None = models.CharField(max_length=255, null=True, blank=True)
    employee_department: str | None = models.CharField(max_length=255, null=True, blank=True)
    employee_number: str | None = models.CharField(max_length=255, null=True, blank=True)
    employee_telephone: str | None = models.CharField(max_length=255, null=True, blank=True)
    employee_title: str | None = models.CharField(max_length=255, null=True, blank=True)
    history: HistoricalRecords = HistoricalRecords(excluded_fields=['history_user'])
    ldap_distinguished_name_dn: str | None = models.CharField(max_length=255, null=True, blank=True)
    person_mapping: Person | None = models.OneToOneField('Person', on_delete=models.SET_NULL, null=True, blank=True, related_name='user')

    def __str__(self):
        return f"{self.last_name}, {self.first_name} - {self.username}"

    class Meta:
        ordering = ['last_name', 'first_name', 'username', '-id']
        verbose_name = "User"
        verbose_name_plural = "Users"
