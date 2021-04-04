from celery import shared_task
import requests

from django.core.mail import send_mail

from .models import Book


@shared_task
def send_mail_task(subject, message, email):
    send_mail(subject, message, email, ['admin@example.com'])


@shared_task
def input_books():
    url = 'http://127.0.0.1:8000/stock/books/'
    response = requests.get(url).json()




