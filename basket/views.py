from datetime import datetime
from itertools import product
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.db import Error
from django.db.models import Sum, Q
from django.contrib.auth.mixins import LoginRequiredMixin
from store.models import Store, StoreProduct

from authentication.models import Order, OrderProduct, OrderStore

from .basket import Basket
from store.models import Product

import json


class BasketView(generic.list.ListView):
    template_name = 'basket/basket.html'
    context_object_name = 'Products'

    def get_queryset(self):
        basket = Basket(self.request)
        return basket

    def get_context_data(self):
        context = super().get_context_data()
        context['Total_price'] = sum(item['total'] for item in context['Products'])
        context['Stores'] = Store.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        basket = Basket(request) 
        data = request.POST
        product_id = int(data['productid'])

        basket.add(product_id=product_id)

        return HttpResponse('1')
    
    def patch(self, request, *args, **kwargs):
        basket = Basket(request)
        data = json.loads(request.body)
        product_id = data['product_id']
        responce_data = {}
        current_amount = basket.basket[str(product_id)]['amount']
        required_amount = int(data['product_amount'])

        product = Product.objects.filter(id=product_id).annotate(
                    overall_amount=Sum('storeproduct__amount', filter=Q(id__exact=product_id))
            )[0]

        difference = required_amount - current_amount
        if product.overall_amount:
            if product.overall_amount >= required_amount and required_amount >= 0:
                basket.update_item(product_id, required_amount)
                responce_data['agreement'] = True
                responce_data['total_product'] = required_amount * product.price
                responce_data['total'] = int(data['total_price']) + difference * product.price
            else:
                responce_data['agreement'] = False
                responce_data['amount'] = current_amount
        else:
            responce_data['agreement'] = 'Out of stock'

        response = JsonResponse(responce_data)
        return response

    def delete(self, request, *args, **kwargs):
        basket = Basket(request)
        data = json.loads(request.body)
        response_data = {}
        product_id = data['product_id']
        total_price = data['total_price']
        current_amount = basket.basket[str(product_id)]['amount']
        
        product = Product.objects.get(id=product_id)

        response_data['total'] = str(int(total_price) - product.price * current_amount)
        
        basket.delete_product(product_id)

        responce = JsonResponse(response_data)
        return responce


class CheckoutRedirectView(LoginRequiredMixin, generic.base.RedirectView):
    pattern_name = 'authentication:profile'

    def get_redirect_url(self, *args, **kwargs):
        kwargs = {}
        return super().get_redirect_url(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        basket = Basket(request)
        order=Order(date=datetime.now())
        order.save()
        result = {}

        for item in basket:
            if item['total_amount'] <= 0:
                basket.delete_product(item['product'].id)
        product_ids = [item['product'].id for item in basket]
        stores = StoreProduct.objects.filter(
            product__in=product_ids
        )
        preferable_stores = stores.filter(
            store__name=kwargs['store']
        ).select_related('product')

        for store in preferable_stores:
            product_id = store.product.id
            amount_needed = basket.basket[str(product_id)]['amount']
            difference = 0
            store.amount -= amount_needed
            if store.amount < 0:
                difference = -store.amount
                store.amount = 0
                result[product_id] = difference
                took = amount_needed - difference
            else:
                took = amount_needed
            order_store = OrderStore(
                order=order,
                storeproduct=store,
                amount=took
                ) 
            order_store.save()
            store.save()
        
        for id in product_ids:
            if id not in result:
                result.update({str(id): basket.basket[str(id)]['amount']})

        remaining_stores = stores.filter(product__in=result.keys()).exclude(
            id__in=preferable_stores
        )

        for store in remaining_stores:
            product_id = store.product.id
            if product_id not in result:
                continue
            if result[product_id] == 0:
                continue
            store.amount -= result[product_id]
            if store.amount < 0:
                difference = -store.amount
                took = result[product_id] - difference
                result[product_id] = -store.amount
                store.amount = 0
            else:
                took = result[product_id]
                result[product_id] = 0
            order_store = OrderStore(
                order=order,
                storeproduct=store,
                amount=took
            )
            order_store.save()
            store.save()
        
        for item in basket:
            order_product = OrderProduct(
                order=order,
                product=item['product'],
                amount=item['amount']
            )
            order_product.save()

        return super().get(request, *args, **kwargs)
