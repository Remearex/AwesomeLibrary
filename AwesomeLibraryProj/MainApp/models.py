from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name"], name="unique_author_name"
            )
        ]
    
class Genre(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name"], name="unique_genre_name"
            )
        ]

class Book(models.Model):
    title = models.CharField(max_length=255)
    pages = models.IntegerField()
    published_by = models.CharField(max_length=255)
    quote = models.CharField(max_length=255)

    authors = models.ManyToManyField(Author, related_name="books", through='BookAuthor')
    genres = models.ManyToManyField(Genre, related_name='books', through='BookGenre')

    def __str__(self):
        return self.title
    
class BookGenre(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)