from django.urls import path

from . import views


app_name = 'store'
urlpatterns = [
    path('', views.index, name='index'),
    path('category/<slug:category_slug>', views.category_list, name='category'),
    path('product_list/<slug:category_slug>', views.product_list, name='product_list'),
]