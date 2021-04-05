from rest_framework import serializers

from .models import Author, Book, Order, OrderItem, Publisher


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'image', 'mark', 'status',
                  'price', 'author', 'pub_year', 'genre', 'publisher']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'book', 'quantity', 'order', 'total_sum']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source="orderitem_set", many=True)

    class Meta:
        model = Order
        fields = ['id', 'user_email', 'user_name', 'status', 'total_sum', 'items']

    def create(self, validated_data):
        valid_data = validated_data.pop('orderitem_set')
        order = Order.objects.create(**validated_data)
        order_items_serializer = self.fields['order_items']
        for each in valid_data:
            each['order'] = order
        order_items_serializer.create(valid_data)
        return order, valid_data


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'pub_title']


