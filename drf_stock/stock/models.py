import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=100)
    author = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.FloatField(max_length=10, validators=[MinValueValidator(1)])
    pub_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(2022)]
    )
    image = models.ImageField(upload_to='static/images')
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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user_email = models.EmailField()
    user_name = models.CharField(max_length=100)
    status = models.PositiveSmallIntegerField(
        choices=Status.choices,
        default=Status.CONSIDERED
    )
    total_sum = models.FloatField(default=0)


class OrderItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_sum = models.FloatField(default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return self.total_sum
