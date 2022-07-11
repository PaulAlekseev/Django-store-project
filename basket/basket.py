from store.models import Product


class Basket:


    def __init__(self, request):
        self.session = request.session
        self.query = None
        basket = self.session.get('basket')
        if 'basket' not in request.session:
            basket = self.session['basket'] = {}
        self.basket = basket

    def add(self, product_id, price):
        product_id = str(product_id)

        if product_id in self.basket:
            self.basket[product_id]['amount'] += 1
        else:
            self.basket[product_id] = {'amount': 1}
        self._save()

    def __iter__(self):
        product_ids = self.basket.keys()

        if self.query is None:
            products = self._get_queryset(product_ids)
        else:
            products = self.query
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product
        
        for item in basket.values():
            item['total'] = item['amount'] * item['product'].price
            yield item

    def clear(self):
        self.basket.clear()

        self._save()

    def update_item(self, data, required_amount):
        product_id = data['product_id']

        self.basket[str(product_id)]['amount'] = required_amount

        self._save()

    def _save(self):
        self.session.modified = True

    def _get_queryset(self, product_ids):
        self.query = Product.objects.filter(id__in=product_ids)
        return self.query