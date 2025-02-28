from simple_history.models import HistoricalRecords

from django.contrib.auth.models import AbstractUser
from core.models.common.abstract.comment import Comment
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
    history = HistoricalRecords(excluded_fields=['history_user'])
    ldap_distinguished_name_dn = create_generic_varchar()
