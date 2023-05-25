"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model
from core.signals import assign_permissions
from django.db.models.signals import post_save

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin page for users."""

    ordering = ['id']
    list_display = ['email', 'phone']
    list_filter = ['is_superuser', 'roles', 'permissions']
    readonly_fields = ['id', 'last_login']

    fieldsets = (
        (None, {
            'fields': (
                'id',
                'email',
                'first_name',
                'last_name',
                'password',
                'phone',
                'is_active',
            ),
        }),
        (_('Roles & Permissions'), {
            'fields': (
                'roles',
                'permissions',
            ),
        }),
        (_('Dates'), {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'roles',
                'permissions',
            ),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        # Make email field read-only during update
        if obj:
            return ['email'] + list(self.readonly_fields)
        return self.readonly_fields

    def has_module_permission(self, request):
        """
        Override the has_module_permission method to allow staff users to access the admin site.
        Only superusers will have full admin privileges.
        """
        return request.user.is_superuser or request.user.is_staff

    def save_related(self, request, form, formsets, change):
        # Call the super method to save related models
        super().save_related(request, form, formsets, change)

        # Get the user instance from the form
        user = form.instance

        # Check if the user has any roles ending with 'Admin' or has 'Admin Permission'
        has_admin_roles = user.roles.filter(name__endswith='Admin').exists()
        has_admin_permission = user.permissions.filter(name='Admin Permission').exists()



        # Determine the values for is_staff and is_superuser
        is_staff = has_admin_roles or has_admin_permission or user.permissions.exists()
        is_superuser = has_admin_roles or has_admin_permission

        # Update the user instance if the values have changed
        if user.is_staff != is_staff or user.is_superuser != is_superuser:
            user.is_staff = is_staff
            user.is_superuser = is_superuser
            user.save(update_fields=['is_staff', 'is_superuser'])

        assign_permissions(sender=get_user_model, instance=user, created=False)



admin.site.register(models.User, UserAdmin)

admin.site.register(models.Role)

admin.site.register(models.Permission)
