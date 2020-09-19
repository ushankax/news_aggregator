from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    source = models.CharField(max_length=55)
    title = models.CharField(max_length=255)
    link = models.URLField(max_length=100)
    text = models.TextField()
    text_preview = models.TextField()

    def __str__(self):
        return "'{}' from {}".format(self.title, self.source)

