from django.db import models
from django.contrib.auth.models import AbstractUser

class BallotRegistration(models.Model):
    ballot_id = models.IntegerField(unique=True)

class UserRegistration(models.Model):
    user_id = models.IntegerField(unique=True)
