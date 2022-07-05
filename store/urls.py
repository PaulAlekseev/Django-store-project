from django.urls import path

from . import views


app_name = 'store'
urlpatterns = [
    path('', views.IndexCategoryView.as_view(), name='index'),
    path('category/<slug:slug>', views.CategoryListView.as_view(), name='category'),
    path('product_list/<slug:category_slug>', views.product_list, name='product_list'),
]