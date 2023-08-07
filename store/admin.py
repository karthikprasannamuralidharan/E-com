from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Contactus)
class contact(admin.ModelAdmin):
    list_display = ['msg_id', 'name', 'email', 'phone', 'desc']


@admin.register(Order)
class Order(admin.ModelAdmin):
    list_display = ['id','customer', 'date_ordered','complete','transaction_id']


@admin.register(Customer)
class customer(admin.ModelAdmin):
    list_display = ['user', 'name', 'email']


@admin.register(OrderItem)
class orderitem(admin.ModelAdmin):
    list_display = ['customer','product', 'order', 'quantity', 'date_added']


@admin.register(Product)
class product(admin.ModelAdmin):
    list_display = ['id','pid', 'name', 'price', 'image']


@admin.register(ShippingAddress)
class shipping(admin.ModelAdmin):
    list_display = ['customer', 'order', 'address', 'city', 'state', 'zipcode', 'date_added']

