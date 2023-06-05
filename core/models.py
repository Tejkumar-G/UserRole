"""
Models for the user role application.
"""
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,
)
from django.db import (
    models,
)


class UserManger(BaseUserManager):
    """User manger class."""

    def create_user(self, email, password=None, **extra_args):
        """Create, save and returns a new user."""
        if not email:
            raise ValueError('User email have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_args)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_args):
        """Create, save and return a new superuser."""
        user = self.create_user(email, password, **extra_args)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


def get_default_group():
    try:
        group = Group.objects.get(name='Default Group')
        return group
    except Group.DoesNotExist:
        return Group.objects.create(name='Default Group')


class User(AbstractBaseUser, PermissionsMixin):
    """User model."""
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(
        max_length=255, unique=True, blank=True, null=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    strategy_access = models.TextField(default="['view']", blank=True)

    objects = UserManger()

    USERNAME_FIELD = 'email'

    # Add a ManyToManyField for groups
    groups = models.ManyToManyField(Group, related_name='users', blank=True)

    def save(self, *args, **kwargs):
        # Call the super method to save the user
        super().save(*args, **kwargs)

        # Assign a default group if no groups are assigned
        if not self.groups.exists():
            default_group = get_default_group()
            self.groups.add(default_group)








