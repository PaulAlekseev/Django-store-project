from django.urls import path

from . import views


app_name = 'basket'
urlpatterns = [
    path('', views.BasketView.as_view(), name='summary'),
    path('add', views.BasketView.as_view(), name='basket_add'),
    path('update', views.BasketView.as_view(), name='basket_update'),
    path('delete', views.BasketView.as_view(), name='basket_delete'),
    path('checkout/<str:store>', views.CheckoutRedirectView.as_view(), name='checkout'),
]
