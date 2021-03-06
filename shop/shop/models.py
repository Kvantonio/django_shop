import uuid

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, URLValidator
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    pub_title = models.CharField(max_length=100)

    def __str__(self):
        return self.pub_title


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.FloatField(max_length=10, validators=[MinValueValidator(1)])
    pub_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(2022)]
    )
    image = models.TextField(validators=[URLValidator()])
    mark = models.FloatField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(5)]
    )
    status = models.BooleanField(default=True)
    genre = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Order(models.Model): # noqa DJ08
    class Status(models.IntegerChoices):
        NO = 0, 'NO Status',
        CONSIDERED = 1, 'Considered',
        IN_PROGRESS = 2, 'In progress',
        DONE = 3, 'Done',

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_sum = models.FloatField(default=0)
    status = models.PositiveSmallIntegerField(
        choices=Status.choices,
        default=Status.NO,
    )

class Item(models.Model): # noqa DJ08
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_sum = models.FloatField(default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
