from urllib import request
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import generic

from store.models import Category
from .basket import Basket


class BasketView(generic.list.ListView):
    template_name = 'basket/basket.html'
    context_object_name = 'Products'

    def get_queryset(self):
        basket = Basket(self.request)
        return basket


def basket_add(request):
    basket = Basket(request) 
    data = request.POST
    if data['action'] == 'post':
        product_id = int(data['productid'])
        product_price = int(data['productprice'])

        basket.add(product_id=product_id, price=product_price)

        return HttpResponse('1')
