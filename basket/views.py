from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import generic

from store.models import Category
from .basket import Basket

import json


class BasketView(generic.list.ListView):
    template_name = 'basket/basket.html'
    context_object_name = 'Products'

    def get_queryset(self):
        basket = Basket(self.request)
        return basket

    def post(self, request, *args, **kwargs):
        basket = Basket(request) 
        data = request.POST
        product_id = int(data['productid'])
        product_price = int(data['productprice'])

        basket.add(product_id=product_id, price=product_price)

        return HttpResponse('1')
    
    def patch(self, request, *args, **kwargs):
        basket = Basket(request)
        data = json.loads(request.body)
        print(data)

        return HttpResponse('1')

