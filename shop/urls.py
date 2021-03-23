from django.conf import settings
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.BookList.as_view(), name="book_list"),
    path('detail/<int:pk>', views.BookDetail.as_view(), name="book_detail"),
]
