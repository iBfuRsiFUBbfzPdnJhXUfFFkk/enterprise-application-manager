from django.db.models import Model, IntegerField


class AbstractGitLabPrimaryKey(Model):
    id: int = IntegerField(primary_key=True)

    class Meta:
        abstract = True
