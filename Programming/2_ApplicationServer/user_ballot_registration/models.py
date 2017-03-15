from django.db import models
from accounts.models import User

class RequestSigniture(models.Model):

    user = models.ForeignKey(User)
    ballot_id = models.IntegerField()
    token = models.CharField(max_length=1000)
    token_signed = models.CharField(max_length=1000)

    class Meta:
        unique_together = ('user', 'ballot_id',)


class RegisterAddress(models.Model):

    user = models.ForeignKey(User)
    ballot_id = models.IntegerField()
    voter_address = models.CharField(max_length=1000)
    voter_private_key = models.CharField(max_length=1000)   # Need to be encrypted with user pass in production
    voter_public_key = models.CharField(max_length=1000)

    class Meta:
        unique_together = ('user', 'ballot_id',)
