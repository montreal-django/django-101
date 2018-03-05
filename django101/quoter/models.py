from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=150)
    birthdate = models.DateField(null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Quote(models.Model):
    quote = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.quote
