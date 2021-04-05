from celery import shared_task

from django.core.mail import send_mail

import requests

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
            author, created = Author.objects.get_or_create(
                id=data['id']
            )

            if not created:
                author.update(name=data['name'])

        if response_author['next']:
            response_author = requests.get(response_author['next']).json()
        else:
            break

    url = 'http://127.0.0.1:8000/stock/publishers/'
    response_publisher = requests.get(url).json()
    while 1:
        for counter, data in enumerate(response_publisher['results']):
            publisher, created = Publisher.objects.get_or_create(
                id=data['id']
            )

            if not created:
                publisher.update(pub_title=data['pub_title'])

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
                    "title": data['title'],
                    "description": data['description'],
                    "image": data['image'],
                    "mark": data['mark'],
                    "status": data['status'],
                    "price": data['price'],
                    "pub_year": data['pub_year'],
                    "genre": data['genre'],
                    "publisher": data['publisher']
                }
            )

            if not created:
                book.update(
                    title=data['title'],
                    description=data['description'],
                    image=data['image'],
                    mark=data['mark'],
                    status=data['status'],
                    price=data['price'],
                    pub_year=data['pub_year'],
                    genre=data['genre'],
                    publisher=data['publisher']
                )

            for i in data['author']:
                author = Author.objects.get(id=i)
                book.add(author)

        if response['next']:
            response = requests.get(response['next']).json()
        else:
            break
