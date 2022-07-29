from django.test import TestCase
from django.urls import reverse

from store.models import Product, StoreProduct, InnerCategory, Store
from basket.basket import Basket

import json


class TestBasketView(TestCase):
    def setUp(self):
        self.category = InnerCategory.objects.create(
            name='Category', slug='Category', features=None
        )
        self.store = Store.objects.create(
            name='SomeStore', location='SomeWhere'
        )
        self.product1 = Product.objects.create(
            name='product1', slug='product1', description='Some description', category_id=self.category.id,
            guarantee=12, features={'feature_field': '2'}, price=399, is_active=True
        )
        self.storeproduct1 = StoreProduct.objects.create(
            product=self.product1, amount=10, store=self.store
        )
        self.storeproduct2 = StoreProduct.objects.create(
            product=self.product1, amount=0, store=self.store
        )
        self.client.post(reverse('basket:basket_add'), {'productid': self.product1.id})

    def test_basket_homepage(self):
        """
        Test homepage status code
        """
        response = self.client.get(reverse('basket:summary'))
        self.assertEqual(response.status_code, 200)

    def test_basket_add(self):
        """
        Test adding item to the basket
        """
        response = self.client.post(reverse('basket:basket_add'), {'productid': self.product1.id})
        basket = Basket(response.wsgi_request)
        self.assertEqual(basket._basket, {'1':{'amount': 2}})

    def test_basket_patch(self):
        """
        Test updating item in the basket
        """
        data = {
            "product_id": self.product1.id,
            "product_amount": 9,
            "total_price": self.product1.price,
        }
        data_json = json.dumps(data)
        response = self.client.patch(reverse('basket:basket_update'), data_json)
        self.assertEqual(response.json(), {
            'agreement': True,
            'total_product': 9*self.product1.price,
            'total': 9*self.product1.price,
        })

        data.update({'product_amount': 20})
        data_json = json.dumps(data)
        response2 = self.client.patch(reverse('basket:basket_update'), data_json)
        self.assertEqual(response2.json(), {
            'agreement': False,
            'amount': 9,
        })

        data.update({'product_amount': -10})
        data_json = json.dumps(data)
        response3 = self.client.patch(reverse('basket:basket_update'), data_json)
        self.assertEqual(response3.json(), {
            'agreement': False,
            'amount': 9,
        })
        
        self.storeproduct1.amount = 0
        self.storeproduct1.save()

        data.update({'product_amount': 5})
        data_json = json.dumps(data)
        response3 = self.client.patch(reverse('basket:basket_update'), data_json)
        self.assertEqual(response3.json(), {
            'agreement': 'Out of stock'
        })