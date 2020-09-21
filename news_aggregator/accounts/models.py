from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User


class Profile(models.Model):
    """Extend base User model"""
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True)
    subscriptions = ArrayField(models.CharField(max_length=255),
                               blank=True)
