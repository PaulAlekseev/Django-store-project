from django.contrib import admin

from .models import Category, Store, Product, PriceStory, StoreProduct, InnerCategory


class PriceInline(admin.TabularInline):
    model = PriceStory
    extra = 1


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


class PriceAdmin(admin.ModelAdmin):
    list_display = ('product', 'date')


class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'category', 'slug']}),
        ('Information', {'fields': ['description', 'guarantee', 'features', 'price']}),
        ('Status', {'fields': ['is_active']}),
    ]
    inlines = [PriceInline, AvailabilityInline]

    list_display = ('name', 'category', 'is_active')

    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(InnerCategory, InnerCategoryAdmin)
admin.site.register(Store)
admin.site.register(Product, ProductAdmin)
admin.site.register(PriceStory, PriceAdmin)
admin.site.register(StoreProduct)
