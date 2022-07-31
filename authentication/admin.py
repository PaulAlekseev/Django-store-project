from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Order, OrderProduct, OrderStore, Review


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'amount')

    ordering = ('-order', )


class OrderStoreAdmin(admin.ModelAdmin):
    list_display = ('order', 'storeproduct', 'amount')

    ordering = ('-order', )


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Order)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(OrderStore, OrderStoreAdmin)
admin.site.register(Review)
