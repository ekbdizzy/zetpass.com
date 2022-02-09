from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class ZetUserManager(BaseUserManager):
    """Django requires define a custom manager with using AbstractBaseUser.
    https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#writing-a-manager-for-a-custom-user-model
    """

    def create_user(self, username, password, **extra_fields):
        """Create and save a User."""
        email = extra_fields.get('email', None)
        if email:
            email = self.normalize_email(email)

        if username is None:
            raise ValueError('The given username must be set')

        if len(username) < 4:
            raise ValueError('The given username must contain at least 4 characters.')

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, password, **extra_fields):
        """Create and save a SuperUser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(password, **extra_fields)


class ZetUser(AbstractBaseUser, PermissionsMixin):
    """User model. Based in AbstractBaseUser because this way seems more obvious
    to redefine email from standard user model and get rid of extra fields."""

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(max_length=150,
                                db_index=True,
                                unique=True,
                                validators=[username_validator])
    email = models.EmailField(max_length=150, null=True, blank=True, unique=True)
    is_active = models.BooleanField(db_index=True, default=True)
    is_staff = models.BooleanField(db_index=True, default=False)
    is_superuser = models.BooleanField(db_index=True, default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = ZetUserManager()

    def __str__(self):
        return self.username
