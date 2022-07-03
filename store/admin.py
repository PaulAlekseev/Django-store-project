from django.contrib import admin

from .models import Category, Store, Product, Price, StoreProduct


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Store)
admin.site.register(Product, ProductAdmin)
admin.site.register(Price)
admin.site.register(StoreProduct)
