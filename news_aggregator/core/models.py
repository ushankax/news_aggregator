from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Article(models.Model):
    source = models.CharField(max_length=55)
    title = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    text = models.TextField()
    import_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "'{}' from {}".format(self.title, self.source)

