from django.db.models import Model, TextField


class Comment(Model):
    comment = TextField(blank=True, null=True)

    class Meta:
        abstract = True