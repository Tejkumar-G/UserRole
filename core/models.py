"""
Models for the user role application.
"""
from django.db import (
    models,
    transaction,
)

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Permission(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


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


def get_default_role():
    try:
        role = Role.objects.get(pk=1)
        return role
    except Role.DoesNotExist:
        return Role.objects.create(id=1, name='default')


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

    objects = UserManger()

    USERNAME_FIELD = 'email'

    roles = models.ManyToManyField(Role, related_name='users', blank=True)
    permissions = models.ManyToManyField(Permission, related_name='users', blank=True)

    @transaction.atomic
    def save(self, *args, **kwargs):
        is_new_user = not self.id

        if is_new_user:
            # If it's a new user, save it first to generate an ID
            super().save(*args, **kwargs)
            self.roles.add(get_default_role())

        super().save(*args, **kwargs)






