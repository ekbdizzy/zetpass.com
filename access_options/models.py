"""Here are the models that are used to control access to credentials."""

from django.db import models
from users.models import ZetUser


class UserIP(models.Model):
    # TODO Add middleware to check and save IP with every request of user.
    """IP-addresses list of user. Also used as allowed IPs in PrivateToken model."""
    pass


class RequestCredentials(models.Model):
    """Requests of credentials. Every request of credentials gets here.
    It is used to indicate to the user what data was requested and when."""
    pass
