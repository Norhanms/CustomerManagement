from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.template import loader
from .filters import OrderFilter
from .forms import OrderForm, CreateUserForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_user


def my_view(request):
    # View code here...
    t = loader.get_template('accounts/index.html')
    c = {'foo': 'bar'}
    return HttpResponse(t.render(c, request), )
# Create your views here.


@login_required(login_url='login_page')
@allowed_user(allowed_roles=['admin'])
def home(request):
    if request.user.is_authenticated:
        logedin = True
        print(request.user.is_authenticated)
    else:
        logedin = False
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='delivered').count()
    pending = orders.filter(status='pending').count()
    context = {
        'orders': orders,
        'customers': customers,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
        'logedin': logedin

    }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login_page')
def products(request):
    if request.user.is_authenticated:
        logedin = True
    else:
        logedin = False
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products, 'logedin': logedin})


@login_required(login_url='login_page')
# @unauthenticated_user
def customer(request, pk_test):
    if request.user.is_authenticated:
        logedin = True
    else:
        logedin = False
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count = customer.order_set.count()  # orders.count()
    myfilter = OrderFilter(request.GET, queryset=orders)
    orders = myfilter.qs
    searchedOrderCount = orders.count()
    context = {
        'customer': customer,
        'orders': orders,
        'order_count': order_count,
        'myfilter': myfilter,
        'searchedOrderCount': searchedOrderCount,
        'logedin': logedin
    }
    return render(request, 'accounts/customer.html', context)


'''
def createOrder(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        # print(request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(customer)
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)
'''
# Multiple forms inside one form using inlineformset_factory


@login_required(login_url='login_page')
def createOrder(request, pk_test):
    if request.user.is_authenticated:
        return redirect(request, 'home')
    else:
        OrderFormSet = inlineformset_factory(
            Customer, Order, fields=('product', 'status'))
        customer = Customer.objects.get(id=pk_test)
        formset = OrderFormSet(instance=customer)
        if request.method == 'POST':
            # print(request.POST)
            form = OrderForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(customer)
        context = {'formset': formset}
        return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login_page')
def updateOrder(request, pk_test):
    order = Order.objects.get(id=pk_test)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form. is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login_page')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'accounts/delete.html', context)


@unauthenticated_user
def register_page(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "account created successfuly!")
        else:
            print("Not valid form")
            messages.error(
                request, "A Problem happend while creating your account")
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        print("post")
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "login successfuly")
            context = {
                'username': user.get_username,
            }
            return redirect('home')
            # return render(request, 'accounts/dashboard.html', context)
        else:
            messages.error(request, "Error while logging in")

    return render(request, 'accounts/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login_page')


def userPage(request):
    return render(request, 'accounts/user.html')
