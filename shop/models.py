from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Author(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    pub_title = models.CharField(max_length=100)

    def __str__(self):
        return self.pub_title


class Books(models.Model):
    title = models.CharField(max_length=100)
    author = models.ManyToManyField(Author)
    publisher = models.OneToOneField(Publisher, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.FloatField(max_length=10, validators=[MinValueValidator(1)])
    pub_year = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(2022)])
    image = models.ImageField(upload_to='static/images', blank=True)
    mark = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    status = models.BooleanField(default=True)
    genre = models.CharField(max_length=200)
