from django.shortcuts import render
from django.views.generic import ListView, DetailView

from shop.models import Books
# Create your views here.


class BookList(ListView):
    model = Books
    template_name = 'shop/books_list.html'


class BookDetail(DetailView):
    model = Books
    template_name = 'shop/book_detail.html'
