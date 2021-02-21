from django.urls import path
from .views import (home, products, customer, createOrder, updateOrder, deleteOrder,
                    my_view, register_page, login_page, logoutUser, userPage)

urlpatterns = [
    path('', home, name='home'),
    path('register', register_page, name='register_page'),
    path('login', login_page, name='login_page'),
    path('logout', logoutUser, name='logout'),
    path('user', userPage, name='user-page'),
    path('products/', products, name='products'),
    path('customer/<str:pk_test>', customer, name='customer'),
    path('create_order/<str:pk_test>', createOrder, name='create_order'),
    path('update_order/<str:pk_test>', updateOrder, name='update_order'),
    path('delete_order/<str:pk>', deleteOrder, name='delete_order'),
    path('index', my_view, name="my_view")
]
