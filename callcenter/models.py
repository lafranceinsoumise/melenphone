from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserExtend(models.Model):
    user = models.OneToOneField(User,related_name="UserExtend",blank=True, null=True)
    agentUsername = models.CharField(max_length=50,blank=True, null=True)
    phi = models.IntegerField(default=0,blank=True, null=True)
    phi_multiplier = models.DecimalField(default=1.0, max_digits=2, decimal_places=1,blank=True, null=True)
    first_call_of_the_day = models.DateTimeField(auto_now=True, blank=True)
    address = models.CharField(max_length=100,blank=True, null=True)
    location_lat = models.CharField(max_length=20, blank=True, null=True)
    location_long = models.CharField(max_length=20, blank=True, null=True)

    def get_achievements(self):
        return self.achievements_aux.all()

class Appel(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    date = models.DateTimeField(auto_now=True, blank=True)

class Achievement(models.Model):
    name = models.CharField(max_length=50)
    condition = models.CharField(max_length=300)
    unlockers = models.ManyToManyField(UserExtend,through='AchievementUnlock', related_name="achievements_aux")

class AchievementUnlock(models.Model):
    userExtend = models.ForeignKey(UserExtend)
    achievement = models.ForeignKey(Achievement)

class NumbersLocation(models.Model):
    code = models.CharField(max_length=6)
    pays = models.CharField(max_length=2)
    zone = models.CharField(max_length=1)
    indicatif = models.CharField(max_length=2)
    location_lat = models.CharField(max_length=20)
    location_long = models.CharField(max_length=20)

    def get_location(self):
        return self.location_lat, self.location_long
