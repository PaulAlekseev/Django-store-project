from django.conf import settings

from store.models import Product


class Basket:

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('basket')
        if 'basket' not in request.session:
            basket = self.session['basket'] = {}
        self.basket = basket

    def _save(self):
        self.session.modified = True

    def add(self, product_id, price):
        product_id = str(product_id)

        if product_id in self.basket:
            self.basket[product_id]['amount'] += 1
        else:
            self.basket[product_id] = {'amount': 1, 'price': price}
        print(self.basket)
        self._save()

    def __iter__(self):
        product_ids = self.basket.keys()

        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]["product"] = product
        
        for item in basket.values():
            item['total'] = item['amount'] * item['price']
            yield item

    def clear(self):
        self.basket.clear()

        self._save()

    # def update():
