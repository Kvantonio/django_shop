from celery import shared_task

from django.core.mail import send_mail

import requests
import uuid

from .models import Author, Book, Publisher


@shared_task
def send_mail_task(subject, message, email):
    send_mail(subject, message, email, ['admin@example.com'])


@shared_task
def input_books():
    url = 'http://127.0.0.1:8000/stock/authors/'
    response_author = requests.get(url).json()
    while 1:
        for counter, data in enumerate(response_author['results']):
            Author.objects.get_or_create(
                id=data['id'],
                defaults={
                    'id': data['id'],
                    'name': data['name']
                }
            )

        if response_author['next']:
            response_author = requests.get(response_author['next']).json()
        else:
            break

    url = 'http://127.0.0.1:8000/stock/publishers/'
    response_publisher = requests.get(url).json()
    while 1:
        for counter, data in enumerate(response_publisher['results']):
            Publisher.objects.get_or_create(
                id=data['id'],
                defaults={
                    'id': data['id'],
                    'pub_title': data['pub_title']
                }
            )

        if response_publisher['next']:
            response_publisher = requests.get(
                response_publisher['next']
            ).json()
        else:
            break

    url = 'http://127.0.0.1:8000/stock/books/'
    response = requests.get(url).json()
    while 1:
        for counter, data in enumerate(response['results']):
            book, created = Book.objects.get_or_create(
                id=data['id'],
                defaults={
                    'id': data['id'],
                    "title": data['title'],
                    "description": data['description'],
                    "image": data['image'],
                    "mark": data['mark'],
                    "status": data['status'],
                    "price": data['price'],
                    "pub_year": data['pub_year'],
                    "genre": data['genre'],
                    "publisher": Publisher.objects.get(id=data['publisher'])
                }
            )

            if not created:
                book.title = data['title']
                book.description = data['description']
                book.image = data['image']
                book.mark = data['mark']
                book.status = data['status']
                book.price = data['price']
                book.pub_year = data['pub_year']
                book.genre = data['genre']
                book.publisher = Publisher.objects.get(id=data['publisher'])
                book.save()

            for i in data['author']:
                author = Author.objects.get(id=i)
                book.author.add(author)

        if response['next']:
            response = requests.get(response['next']).json()
        else:
            break
