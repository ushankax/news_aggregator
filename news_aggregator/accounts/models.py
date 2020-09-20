from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """Extend base User model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    subscriptions = ArrayField(models.CharField(max_length=255), blank=True)

