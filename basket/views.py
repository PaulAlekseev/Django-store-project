from django.shortcuts import render
from django.views import generic

from store.models import Category
from .basket import Basket


class BasketView(generic.list.ListView):
    template_name = 'basket/basket.html'
    model = Category

    def get(self, request, *args, **kwargs):
        # a = Basket(request)
        return super().get(self, request, *args, **kwargs)

