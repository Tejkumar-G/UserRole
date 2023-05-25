"""
Signal for User object to update the roles and the permissions.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model

@receiver(post_save, sender=User)
def assign_permissions(sender, instance, created, **kwargs):
    if not created:
        # Clear all existing user permissions
        instance.user_permissions.clear()

        # Assign permissions based on user roles and selected permissions
        permissions = get_assigned_permissions(instance)

        if permissions:
            # Assign the permissions to the user
            instance.user_permissions.set(permissions)


def get_assigned_permissions(user):
    permissions = set()

    if has_admin_roles(user):
        # User has admin roles, assign all permissions
        permissions.update(get_all_permissions())
        return

    if has_client_permissions(user):
        # User has client permissions, assign client permissions
        permissions.update(get_client_permissions())

    if has_strategy_permissions(user) or has_strategy_roles(user):
        # User has strategy permissions or strategy roles, assign strategy permissions
        permissions.update(get_strategy_permissions())

    return permissions

def has_admin_roles(user):
    return user.permissions.filter(name__startswith='Admin').exists()

def has_client_permissions(user):
    return user.permissions.filter(name__startswith='Client').exists()

def has_strategy_permissions(user):
    return user.permissions.filter(name__startswith='Strategy').exists()

def has_strategy_roles(user):
    return user.roles.filter(name__startswith='Strategy').exists()

def get_all_permissions():
    return Permission.objects.all()

def get_client_permissions():
    return Permission.objects.filter(codename__in=['view_user', 'add_user', 'change_user', 'delete_user'])

def get_strategy_permissions():
    return Permission.objects.filter(codename__in=['view_strategy', 'add_strategy', 'change_strategy', 'delete_strategy'])



