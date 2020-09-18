from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return self.title

