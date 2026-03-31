from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)  # optional
    published_year = models.IntegerField()
    isbn = models.CharField(max_length=20, blank=True, null=True)  # optional

    def __str__(self):
        return self.title
