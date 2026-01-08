from django import forms
from django.db import models

from core.forms.common.base_model_form import BaseModelForm
from core.forms.common.base_model_form_meta import BaseModelFormMeta
from core.models.bookmark_folder import BookmarkFolder


class BookmarkFolderForm(BaseModelForm):
    """Form for creating/editing bookmark folders."""

    class Meta(BaseModelFormMeta):
        model = BookmarkFolder
        fields = ['name', 'parent_folder', 'color']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        # Only show user's own folders as parent options
        # Exclude self and descendants to prevent circular references
        queryset = BookmarkFolder.objects.filter(user=user)
        if self.instance and self.instance.pk:
            # Exclude self
            queryset = queryset.exclude(pk=self.instance.pk)
            # Exclude all descendants
            descendants = self.instance.get_all_children_recursive
            if descendants:
                queryset = queryset.exclude(pk__in=[d.pk for d in descendants])

        self.fields['parent_folder'].queryset = queryset
        self.fields['parent_folder'].required = False
        self.fields['parent_folder'].label = "Parent Folder (optional)"

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user

        # Auto-assign order (append to end)
        if not instance.order:
            siblings = BookmarkFolder.objects.filter(
                user=self.user,
                parent_folder=instance.parent_folder
            )
            max_order = siblings.aggregate(models.Max('order'))['order__max'] or 0
            instance.order = max_order + 1

        if commit:
            instance.save()
        return instance
