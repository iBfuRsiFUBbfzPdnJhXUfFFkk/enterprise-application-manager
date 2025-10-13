from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.forms.common.generic_choice_field import generic_choice_field
from core.forms.common.generic_date_field import generic_date_field
from core.forms.common.generic_multiple_choice_field import generic_multiple_choice_field
from core.models.application import Application
from core.models.job_level import JobLevel
from core.models.job_title import JobTitle
from core.models.person import Person
from core.models.role import Role
from core.models.skill import Skill


class PersonForm(BaseModelForm):
    applications_developer_of = generic_multiple_choice_field(queryset=Application.objects.all())
    applications_stakeholder_of = generic_multiple_choice_field(queryset=Application.objects.all())
    date_birthday = generic_date_field()
    date_hired = generic_date_field()
    date_left = generic_date_field()
    job_level = generic_choice_field(queryset=JobLevel.objects.all())
    job_title = generic_choice_field(queryset=JobTitle.objects.all())
    roles = generic_multiple_choice_field(queryset=Role.objects.all())
    skills = generic_multiple_choice_field(queryset=Skill.objects.all())

    class Meta(BaseModelFormMeta):
        model = Person
