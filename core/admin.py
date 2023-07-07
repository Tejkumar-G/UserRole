"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import (
    Permission,
    Group,
)
from django.utils.translation import gettext_lazy as _

from core import models
from core.forms import StrategyAccessForm


class UserAdmin(BaseUserAdmin):
    """Define the admin page for users."""
    form = StrategyAccessForm

    ordering = ['id']
    list_display = ['email', 'phone']
    list_filter = ['is_superuser']
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
                'is_staff',
                'is_superuser',
                'strategy_access',
            ),
        }),
        (_('Groups'), {
            'fields': (
                'groups',
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
                'groups',
                'is_staff',
                'is_superuser',
                'strategy_access',
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

        # Get the default group and its associated permissions
        default_group = Group.objects.get(name='Default Group')
        default_group_permissions = default_group.permissions.all()

        # Get all permissions except for the default group permissions
        excluded_permissions = Permission.objects.exclude(id__in=default_group_permissions)

        try:
            # Check if the user has other permissions besides the default group
            has_other_permissions = user.groups.permissions.filter(id__in=excluded_permissions).exists()

            # Update the user instance if the values have changed
            if has_other_permissions:
                user.is_staff = True
                user.is_superuser = excluded_permissions.count() == user.groups.permissions.count()
                user.save(update_fields=['is_staff', 'is_superuser'])
        except Exception as e:
            print(e)

        # Assign permissions based on the user's role and selected permissions
        # assign_permissions(sender=get_user_model, instance=user, created=False)



admin.site.register(models.User, UserAdmin)


admin.site.register(Permission)
