from typing import Optional

from django.contrib.auth.models import AbstractUser
from simple_history.models import HistoricalRecords

from core.models.common.abstract.comment import Comment
from core.models.common.field_factories.create_generic_one_to_one_fk import create_generic_one_to_one_fk
from core.models.common.field_factories.create_generic_uuid import create_generic_uuid
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar


class User(AbstractUser, Comment):
    active_directory_globally_unique_identifier_guid = create_generic_varchar()
    active_directory_security_accounts_manager_account_name = create_generic_varchar()
    active_directory_security_accounts_manager_account_type = create_generic_varchar()
    active_directory_security_identifier_sid = create_generic_varchar()
    employee_company = create_generic_varchar()
    employee_department = create_generic_varchar()
    employee_number = create_generic_varchar()
    employee_telephone = create_generic_varchar()
    employee_title = create_generic_varchar()
    enumeration_attack_uuid = create_generic_uuid()
    history = HistoricalRecords(excluded_fields=['history_user'])
    ldap_distinguished_name_dn = create_generic_varchar()
    person_mapping = create_generic_one_to_one_fk(related_name="user_mapping", to='Person')

    @staticmethod
    def get_by_uuid(uuid: str) -> Optional['User']:
        return User.objects.filter(enumeration_attack_uuid=uuid).first()
