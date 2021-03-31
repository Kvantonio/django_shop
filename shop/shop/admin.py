from django.contrib import admin

from .models import Author, Book, Publisher


@admin.register(Book)
class BooksAdmin(admin.ModelAdmin):
    fields = ['title', 'description', 'image', 'mark', 'status', 'price',
              'author', 'pub_year', 'genre', 'publisher']
    list_display = ['title', 'description', 'image', 'mark', 'status', 'price',
                    'pub_year', 'genre', 'publisher']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['name']


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    fields = ['pub_title']
    list_display = ['pub_title']
