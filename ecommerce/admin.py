from django.contrib import admin
from .models import (
    Order,
    OrderItems,
    ShippingAddress,
)
# Register your models here.


class OrderAdminView(admin.ModelAdmin):
    list_display = ('id','customer','date','complete','transaction_id')


class OrderItemsAdminView(admin.ModelAdmin):
    list_display = ('id','order','product','quantity')


class ShippingAddressAdminView(admin.ModelAdmin):
    list_display = ('id','customer','order','address','city','state','city','state','zipcode')



admin.site.register(Order,OrderAdminView)
admin.site.register(OrderItems,OrderItemsAdminView)
admin.site.register(ShippingAddress,ShippingAddressAdminView)