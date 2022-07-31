from django.contrib import admin

from .models import Category, Store, Product, StoreProduct, InnerCategory


class AvailabilityInline(admin.TabularInline):
    model = StoreProduct
    extra = 1


class InnerCategoriesInline(admin.TabularInline):
    model = InnerCategory
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    inlines = [InnerCategoriesInline]
    prepopulated_fields = {'slug': ('name',)}


class InnerCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'category', 'image', 'slug']}),
        ('Information', {'fields': [
            'description', 'guarantee', 'features', 'price'
        ]}),
        ('Status', {'fields': ['is_active']}),
    ]
    inlines = [AvailabilityInline, ]

    list_display = ('name', 'category', 'is_active')

    prepopulated_fields = {"slug": ("name",)}


class StoreProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'store', 'amount')

    ordering = ('-product', )


admin.site.register(Category, CategoryAdmin)
admin.site.register(InnerCategory, InnerCategoryAdmin)
admin.site.register(Store)
admin.site.register(Product, ProductAdmin)
admin.site.register(StoreProduct, StoreProductAdmin)
