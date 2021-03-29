from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView, ListView

from shop.models import Books, Cart, Item


# Create your views here.


class BookList(ListView):
    model = Books
    template_name = 'shop/books_list.html'


class BookDetail(DetailView):
    model = Books
    template_name = 'shop/book_detail.html'


def success(request):
    return HttpResponse("SUCCESS!!!")


class LoginForm(LoginView):
    model = User
    template_name = "registration/login.html"
    success_url = 'shop/'

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Authorization success!'
        )
        return HttpResponseRedirect(self.get_success_url())


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/shop/success/')


class RegistrationForm(CreateView):
    model = User
    template_name = "registration/registration.html"
    fields = ['username', 'email', 'password', 'first_name', 'last_name']
    success_url = '/shop/login/'

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        user = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        User.objects.create_user(
            username=user,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Registration success!'
        )
        return redirect(self.success_url)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request,
                'Your password was successfully updated!'
            )
            return redirect('shop:login')
        else:
            messages.error(
                request,
                'Please correct the error below.'
            )
    else:
        form = PasswordChangeForm(request.user)
    return render(request,
                  'registration/password_change_form.html',
                  {'form': form})


class CartDetailView(DetailView):
    model = Cart


class CartCreate(CreateView):
    pass

def add_to_cart(request, pk):
    count = 1
    user = request.user
    item, created = Item.objects.get_or_create(
        user=user,
        book=Books.objects.get(pk=pk),
    )

    if not created:
        item = Item(
            user=user,
            book=Books.objects.get(pk=pk),
            quantity=item.quantity + count
        )
    item.save()

    cart, created = Cart.objects.get_or_create(
        user=user
    )

    if not created:
        cart = Cart(
            product=item,
            total_books=item.quantity,
            total_price=item.book.price,
            user=user
        )
    cart.save()
    return redirect('shop:cart')
