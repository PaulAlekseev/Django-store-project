from django.urls import path

from . import views


app_name = 'store'
urlpatterns = [
    path('', views.IndexCategoryView.as_view(), name='index'),
    path('category/<slug:slug>', views.CategoryListView.as_view(), name='category'),
    path('product_list/<slug:category_slug>', views.ProductListView.as_view(), name='product_list'),
    path('product/<slug:slug>', views.ProductDetailView.as_view(), name='product_detail'),
    path('prodcut/filters/send/<slug:slug>', views.ProductListView.as_view(), name='filter')
]