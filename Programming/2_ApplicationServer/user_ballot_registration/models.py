from django.db import models
from accounts.models import User

# Create your models here.
class RequestSigniture(models.Model):

    user = models.ForeignKey(User)
    ballot_id = models.IntegerField()
    token = models.IntegerField()
    token_signed = models.IntegerField()

    class Meta:
        unique_together = ('user', 'ballot_id',)
