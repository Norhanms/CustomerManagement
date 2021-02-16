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


def my_view(request):
    # View code here...
    t = loader.get_template('accounts/index.html')
    c = {'foo': 'bar'}
    return HttpResponse(t.render(c, request), )
# Create your views here.


def home(request):
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
        'pending': pending

    }
    return render(request, 'accounts/dashboard.html', context)


def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


def customer(request, pk_test):
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
        'searchedOrderCount': searchedOrderCount
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


def createOrder(request, pk_test):
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


def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'accounts/delete.html', context)


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
                'username': user.get_username
            }
            return redirect('home')
            # return render(request, 'accounts/dashboard.html', context)
        else:
            messages.error(request, "Error while logging in")

    return render(request, 'accounts/login.html')
