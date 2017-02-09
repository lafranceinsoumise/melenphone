from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class UserExtend(models.Model):
    user = models.OneToOneField(User,related_name="UserExtend")
    agentUsername = models.CharField(max_length=50)
    phi = models.IntegerField()
    ville = models.CharField(max_length=50)

class Appel(models.Model):
    user = models.ForeignKey(User)
