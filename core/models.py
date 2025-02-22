from django.db.models import Model, CharField, ForeignKey, DO_NOTHING, ManyToManyField


class Display(Model):
    display_label = CharField(max_length=255, null=True)

    class Meta:
        abstract = True


class Person(Display):
    name_first = CharField(max_length=255, null=True)
    name_last = CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.name_last} {self.name_first} - {self.display_label}"


class Application(Display):
    acronym = CharField(max_length=255, null=True)
    person_architect = ForeignKey(**{
        "null": True,
        "on_delete": DO_NOTHING,
        "related_name": 'applications_as_architect',
        "to": Person,
    })
    person_developers = ManyToManyField(**{
        "to": Person,
    })
    person_lead_developer = ForeignKey(**{
        "null": True,
        "on_delete": DO_NOTHING,
        "related_name": 'applications_as_lead_developer',
        "to": Person,
    })
    person_product_manager = ForeignKey(**{
        "null": True,
        "on_delete": DO_NOTHING,
        "related_name": 'applications_as_product_manager',
        "to": Person,
    })
    person_product_owner = ForeignKey(**{
        "null": True,
        "on_delete": DO_NOTHING,
        "related_name": 'applications_as_product_owner',
        "to": Person,
    })
    person_project_manager = ForeignKey(**{
        "null": True,
        "on_delete": DO_NOTHING,
        "related_name": 'applications_as_project_manager',
        "to": Person,
    })
    person_scrum_master = ForeignKey(**{
        "null": True,
        "on_delete": DO_NOTHING,
        "related_name": 'applications_as_scrum_master',
        "to": Person,
    })

    def __str__(self):
        return f"{self.display_label} ({self.acronym})"
