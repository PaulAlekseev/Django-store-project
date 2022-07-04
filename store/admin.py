from django.contrib import admin

from .models import Category, Store, Product, Price, StoreProduct


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class PriceAdmin(admin.ModelAdmin):
    list_display = ('product', 'date')


class PriceInline(admin.TabularInline):
    model = Price
    extra = 1


class AvailabilityInline(admin.TabularInline):
    model = StoreProduct
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'category', 'slug']}),
        ('Information', {'fields': ['description', 'guarantee', 'features', ]}),
        ('Status', {'fields': ['is_active']}),
    ]
    inlines = [PriceInline, AvailabilityInline]

    list_display = ('name', 'category', 'is_active')

    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Store)
admin.site.register(Product, ProductAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(StoreProduct)
