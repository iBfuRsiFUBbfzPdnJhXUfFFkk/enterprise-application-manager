from django.contrib.auth.models import AbstractUser
from simple_history.models import HistoricalRecords

from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_enumeration_attack_uuid import AbstractEnumerationAttackUuid
from core.models.common.field_factories.create_generic_one_to_one_fk import create_generic_one_to_one_fk
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar
from core.models.person import Person


class User(
    AbstractComment,
    AbstractEnumerationAttackUuid,
    AbstractUser,
):
    active_directory_globally_unique_identifier_guid: str | None = create_generic_varchar()
    active_directory_security_accounts_manager_account_name: str | None = create_generic_varchar()
    active_directory_security_accounts_manager_account_type: str | None = create_generic_varchar()
    active_directory_security_identifier_sid: str | None = create_generic_varchar()
    employee_company: str | None = create_generic_varchar()
    employee_department: str | None = create_generic_varchar()
    employee_number: str | None = create_generic_varchar()
    employee_telephone: str | None = create_generic_varchar()
    employee_title: str | None = create_generic_varchar()
    history: HistoricalRecords = HistoricalRecords(excluded_fields=['history_user'])
    ldap_distinguished_name_dn: str | None = create_generic_varchar()
    person_mapping: Person | None = create_generic_one_to_one_fk(to='Person')

    def __str__(self):
        return f"{self.last_name}, {self.first_name} - {self.username}"

    class Meta:
        ordering = ['last_name', 'first_name', 'username', '-id']
        verbose_name = "User"
        verbose_name_plural = "Users"
