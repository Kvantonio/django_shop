from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.BookList.as_view(), name="book_list"),
    path('detail/<int:pk>', views.BookDetail.as_view(), name="book_detail"),
    path('success/', views.success, name='success'),
    path('login/', views.LoginForm.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registrate/', views.RegistrationForm.as_view(), name='registrate'),
    path('password_update/', views.change_password, name='change-password'),
    path('cart/', views.CartDetailView.as_view(), name='cart'),
    path('cart/<int:pk>', views.add_to_cart, name='cart-create'),
    path('cart-del/<int:pk>', views.del_item_cart, name='cart-delete'),
    path('order_send/', views.order_send, name='order-send'),

    path('change_password/', views.change_password, name='change_password'),
    path('search-res/',
         views.SearchResultView.as_view(),
         name='search_results'),

]
