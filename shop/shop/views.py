from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models import Q, Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView, ListView

from shop.models import Book, Item


# Create your views here.


class BookList(ListView):
    model = Book
    template_name = 'shop/books_list.html'


class BookDetail(DetailView):
    model = Book
    template_name = 'shop/book_detail.html'


def success(request):
    return HttpResponse("SUCCESS!!!")


class LoginForm(LoginView):
    model = User
    template_name = "registration/login.html"
    success_url = '/shop/'

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Authorization success!'
        )
        return HttpResponseRedirect(self.success_url)


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


class CartListView(ListView):
    model = Item

    def get_queryset(self):
        return super(CartListView, self)\
            .get_queryset()\
            .filter(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_total_price = Item.objects\
            .filter(user=self.request.user)\
            .aggregate(Sum('total_sum'))

        context['cart_total'] = cart_total_price['total_sum__sum']
        return context


def add_to_cart(request, pk):
    user = request.user
    item, created = Item.objects.get_or_create(
        user=user,
        book=Book.objects.get(pk=pk),
        defaults={'total_sum': Book.objects.get(pk=pk).price},
    )

    if not created:
        item.quantity += 1
        item.total_sum += item.book.price
        item.save()

    return redirect('shop:cart')


def del_item_cart(request, pk):
    item = Item.objects.get(id=pk)
    if item.quantity > 1:
        item.quantity -= 1
        item.total_sum -= item.book.price
        item.save()
    else:
        item.delete()
    return redirect('shop:cart')


class SearchResultView(ListView):
    model = Book
    template_name = 'store/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Book.objects.filter(
            Q(title__contains=query) | Q(genre__contains=query)
        )
        return object_list
