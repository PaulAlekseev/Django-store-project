from copy import deepcopy

from django.db.models import Sum

from store.models import Product


class Basket:
    """
    Represents basket with products that user wants to buy
    """
    def __init__(self, request):
        self.session = request.session
        self.query = None
        self._changed = True
        basket = self.session.get('basket')
        if 'basket' not in request.session:
            basket = self.session['basket'] = {}
        self._basket = basket

    def add(self, product_id):
        """
        Adds product to the basket depending on its id
        """
        product_id = str(product_id)

        if product_id in self._basket:
            self._basket[product_id]['amount'] += 1
        else:
            self._basket[product_id] = {'amount': 1}
        self._save()

    def update_item(self, product_id, required_amount):
        """
        Updates product amount information
        """
        self._basket[str(product_id)]['amount'] = required_amount

        self._changed = True
        self._save()

    def delete_product(self, product_id):
        """
        Deletes a product from the basket
        """
        del self._basket[str(product_id)]

        self._changed = True
        self._save()

    def clear(self):
        """
        Clears basket
        """
        self._changed = True
        self._basket.clear()

    def __iter__(self):
        product_ids = self._basket.keys()

        if self.query is None or self._changed:
            self._new_queryset(product_ids)
            self._changed = False
        products = self.query
        basket = deepcopy(self._basket)

        for product in products:
            basket[str(product.id)]['product'] = product
            basket[str(product.id)]['total_amount'] = product.total_amount if product.total_amount is not None else 0

        for item in basket.values():
            if item['amount'] > item['total_amount']:
                item['amount'] = item['total_amount']
                self._basket[str(item['product'].id)]['amount'] = item['total_amount']
                self._save()
            item['total'] = item['amount'] * item['product'].price
            yield item

    def __len__(self):
        return len(self._basket)

    def __getitem__(self, key):
        return self._basket[key]

    def _save(self):
        self.session.modified = True

    def _new_queryset(self, product_ids):
        self.query = Product.objects.filter(id__in=product_ids).annotate(
            total_amount=Sum('storeproduct__amount')
        )
