from rest_framework import serializers

from .models import Author, Book, Order, OrderItem, Publisher


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'description', 'image', 'mark', 'status', 'price',
                  'author', 'pub_year', 'genre', 'publisher']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['user_email', 'user_name', 'status', 'total_sum']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name']


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['pub_title']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['book', 'quantity', 'order', 'total_sum']
