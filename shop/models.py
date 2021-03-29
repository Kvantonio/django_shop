from django.contrib.auth.models import User
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


class Books(models.Model):
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


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    all_price = models.FloatField(default=0)

    def __str__(self):
        return self.all_price


class Item(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return self.book
