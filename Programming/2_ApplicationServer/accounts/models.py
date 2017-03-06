from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    force_enterDetails = models.BooleanField(default=False)

    def getForceEnterDetails(self):
        return self.force_enterDetails
