from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.http import HttpRequest

from core.admin.base_model_admin import BaseModelAdmin
from core.models.role import Role


class RoleAdmin(BaseModelAdmin):
    """
    Custom admin for Role model that prevents deletion of protected roles.
    """
    list_display = ['name', 'acronym', 'is_protected', 'id']
    list_filter = ['is_protected']
    readonly_fields = ['is_protected']  # Make is_protected read-only in admin

    def has_delete_permission(self, request: HttpRequest, obj: Role | None = None) -> bool:
        """
        Prevent deletion of protected roles through the admin interface.
        """
        if obj is not None and obj.is_protected:
            return False
        return super().has_delete_permission(request, obj)

    def delete_model(self, request: HttpRequest, obj: Role) -> None:
        """
        Override delete_model to show a user-friendly error message.
        """
        if obj.is_protected:
            messages.error(
                request,
                f"Cannot delete protected role '{obj.name}'. "
                f"This role is required by the application."
            )
            return
        try:
            super().delete_model(request, obj)
            messages.success(request, f"Successfully deleted role '{obj.name}'.")
        except ValidationError as e:
            messages.error(request, str(e))

    def delete_queryset(self, request: HttpRequest, queryset) -> None:
        """
        Override bulk delete to prevent deletion of protected roles.
        """
        protected_roles = queryset.filter(is_protected=True)
        if protected_roles.exists():
            protected_names = ', '.join([role.name for role in protected_roles])
            messages.error(
                request,
                f"Cannot delete protected roles: {protected_names}. "
                f"These roles are required by the application."
            )
            # Only delete non-protected roles
            queryset = queryset.filter(is_protected=False)

        if queryset.exists():
            count = queryset.count()
            try:
                super().delete_queryset(request, queryset)
                messages.success(request, f"Successfully deleted {count} role(s).")
            except ValidationError as e:
                messages.error(request, str(e))


# Unregister the default admin if it exists and register the custom one
try:
    admin.site.unregister(Role)
except admin.sites.NotRegistered:
    pass

admin.site.register(Role, RoleAdmin)
