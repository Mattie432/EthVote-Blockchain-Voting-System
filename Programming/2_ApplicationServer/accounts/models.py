from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Here we extend the default user class to add our custom fields.
    """
    force_enterDetails = models.BooleanField(default=True)
    username = models.IntegerField(unique=True)
    USERNAME_FIELD = 'username'

    def getForceEnterDetails(self):
        return self.force_enterDetails
