from django.contrib import admin
from .models import Order, OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'paid_amount']
    search_fields = ( 'user', 'paid_amount',)
    list_per_page = 20


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product','order', 'quantity']
    search_fields = ( 'product',)


admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)