from django.contrib import admin

from .models import Author, Books, Item, Publisher


@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    fields = ['title', 'description', 'image', 'mark', 'status', 'price',
              'author', 'pub_year', 'genre', 'publisher']
    list_display = ['title', 'description', 'image', 'mark', 'status', 'price']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['name']


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    fields = ['pub_title']
    list_display = ['pub_title']



@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    fields = ['book', 'quantity', 'user']
    list_display = ['book', 'quantity', 'user']
