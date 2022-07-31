from .filter_handlers import filter_keyword_dictionary


class ProductFormer:

    def __init__(self, filter_handlers):
        self._filter_handlers = filter_handlers
        self._query = None
        self._filters = None

    def _form_product(self):
        filter_dict = {}
        for key, item in self._filters.items():
            if key in self._filter_handlers:
                filter_dict.update(self._filter_handlers[key].transform_filter(item))
        products = self._query.filter(**filter_dict)
        return products

    def get_products(self, product_queryset, filters):
        self._query = product_queryset
        self._filters = filters
        products = self._form_product()
        return products


product_former = ProductFormer(filter_keyword_dictionary)
