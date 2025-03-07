from typing import Optional

from django.contrib.auth.models import AbstractUser
from simple_history.models import HistoricalRecords

from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_enumeration_attack_uuid import AbstractEnumerationAttackUuid
from core.models.common.field_factories.create_generic_one_to_one_fk import create_generic_one_to_one_fk
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar


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
    history = HistoricalRecords(excluded_fields=['history_user'])
    ldap_distinguished_name_dn = create_generic_varchar()
    person_mapping = create_generic_one_to_one_fk(related_name="user_mapping", to='Person')

    @staticmethod
    def get_by_uuid(uuid: str) -> Optional['User']:
        return User.objects.filter(enumeration_attack_uuid=uuid).first()
