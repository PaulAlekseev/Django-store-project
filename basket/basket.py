from django.conf import settings


class Basket:

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('basket')
        if 'basket' not in request.session:
            basket = self.session['basket'] = {}
        self.basket = basket
        print(self.basket is request.session.get('basket'))

    def _save(self):
        self.session.modified = True

    # def add(self, product):
    #     product_id = product.id
    #
    #     if product_id not in self.basket:
    #
    #
    #     self._save()