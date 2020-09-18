from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=255)
    link = models.CharField(max_length=55)
    text = models.TextField()

    def __str__(self):
        return self.title

