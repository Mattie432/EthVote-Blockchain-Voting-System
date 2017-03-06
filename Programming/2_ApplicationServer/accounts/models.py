from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    force_enterDetails = models.BooleanField(default=True)

    def getForceEnterDetails(self):
        return self.force_enterDetails
