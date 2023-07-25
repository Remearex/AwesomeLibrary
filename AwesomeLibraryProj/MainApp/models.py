from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Genre(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    pages = models.IntegerField()
    published_by = models.CharField(max_length=100)
    quote = models.CharField(max_length=500)

    authors = models.ManyToManyField(Author, related_name="books")
    genres = models.ManyToManyField(Genre, related_name='books')

    def __str__(self):
        return self.title