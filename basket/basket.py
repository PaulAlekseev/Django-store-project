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

    def add(self, product_id):
        product_id = str(product_id)

        if product_id in self.basket:
            self.basket[product_id] += 1
        else:
            self.basket[product_id] = 1
        self._save()
