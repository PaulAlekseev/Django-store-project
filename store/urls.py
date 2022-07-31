from django.urls import path, re_path

from . import views


app_name = 'store'
urlpatterns = [
    path('', views.IndexCategoryView.as_view(), name='index'),
    path('category/<slug:slug>', views.CategoryListView.as_view(), name='category'),
    re_path(r'^product_list/(?P<category_slug>[\w-]+)/(?:\??(?P<filters>[\w~@=&-]+)?)$', views.ProductListView.as_view(), name='filtered_product_list'),
    path('product/<slug:slug>', views.ProductDetailView.as_view(), name='product_detail'),
    path('product/filters/send/<slug:slug>', views.ProductListView.as_view(), name='filter'),
    path('search/', views.SearchListView.as_view(), name='search'),
]
