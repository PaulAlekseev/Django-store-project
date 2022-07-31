from django.test import TestCase

from ..models import InnerCategory, Product, Store, StoreProduct


class TestStoreModels(TestCase):

    def setUp(self):
        self.category = InnerCategory.objects.create(
            name='Category', slug='Category', features=None
        )
        self.product = Product.objects.create(
            name='Product', slug='Product', guarantee=12, price=399, category=self.category,
            features={'feature1': 2, 'feature2': 3, 'feature3': 'Nineteen'}
        )

    def test_store_category_model_prepopulated_features(self):
        """
        Test for inner categories prepopulated features
        """

        self.assertEqual(self.category.features, {'fields': {}, 'requested_fields': []})

    def test_store_product_model_save_mathod(self):
        """
        Test for Product save method effect on Inner category features field
        """
        self.category.features.update({'fields': {}, 'requested_fields': ['feature1', 'feature3']})
        self.category.save()
        Product.objects.create(
            name='Product2', slug='Product2', guarantee=12, price=399, category=self.category,
            features={'feature1': 3, 'feature2': 4, 'feature3': 'four'}
        )

        category = InnerCategory.objects.all()[0]

        self.assertEqual(category.features['fields'], {'feature1': ['2', '3'], 'feature3': ['Nineteen', 'four']})

    def test_store_inner_category_model_save_method_on_delete(self):
        """
        Test for Inner category save method with deleted feature requested fields
        """
        self.category.features.update({'requested_fields': ['feature1', 'feature2']})
        self.category.save()
        self.category.features.update({'requested_fields': ['feature1']})
        self.category.save()

        category1 = InnerCategory.objects.get(id=self.category.id)

        self.assertEqual(category1.features['fields'], {'feature1': ['2']})

    def test_store_inner_category_model_save_method_on_updating(self):
        """
        Test for Inner category save method with addition of feature requested fields
        """
        Product.objects.create(
            name='Product1', slug='Product1', guarantee=12, price=399, category=self.category,
            features=None
        )
        self.category.features.update({'requested_fields': ['feature1', 'feature2']})
        self.category.save()

        category1 = InnerCategory.objects.get(id=self.category.id)

        self.assertEqual(category1.features['fields'], {'feature1': ['2'], 'feature2': ['3']})

    def test_category_on_save_method_with_product_none_fields(self):
        """
        Test category model save method with one of products having None feature requested field
        """
        self.category.features.update({'requested_fields': ['feature1', 'feature2', 'feature3', 'feature4']})
        self.category.save()
        Product.objects.create(
            name='Product1', slug='Product1', guarantee=12, price=399, category=self.category,
            features={'feature1': 2, 'feature2': 4, 'feature3': 'five'}
        )

        category1 = InnerCategory.objects.get(id=self.category.id)

        self.assertEqual(category1.features['fields'], {
            'feature1': ['2'], 'feature2': ['3', '4'], 'feature3': ['Nineteen', 'five'], 'feature4': []
            })

    def test_storeproduct_string_method(self):
        """
        Test on storeproduct string method
        """
        store = Store.objects.create(name='Store', location='Location')
        store_product = StoreProduct.objects.create(
            store=store, product=self.product, amount=2
        )
        store_product_string = str(store_product)

        self.assertEqual(store_product_string, self.product.name + ' from ' + store.name)

    def test_product_string(self):
        """
        Test on product string method
        """
        product_string = str(self.product)

        self.assertEqual(product_string, self.product.name)

    def test_store_string(self):
        """
        Test on store string method
        """
        store = Store.objects.create(name='Store', location='Location')
        store_string = str(store)

        self.assertEqual(store_string, store.name)
