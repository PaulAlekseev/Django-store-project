from django.test import TestCase
from django.urls import reverse

from store.models import Product, StoreProduct, InnerCategory, Store
from authentication.models import CustomUser, Order, OrderProduct, OrderStore
from basket.basket import Basket

import json


class TestBasketView(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user('User1', 'email2@mail.com', 'User1password')
        self.category = InnerCategory.objects.create(
            name='Category', slug='Category', features=None
        )
        self.store1 = Store.objects.create(
            name='SomeStore', location='SomeWhere'
        )
        self.store2 = Store.objects.create(
            name='SomeStore2', location='SomeWhere2'
        )
        self.store3 = Store.objects.create(
            name='SomeStore3', location='SomeWhere3'
        )
        self.product1 = Product.objects.create(
            name='product1', slug='product1', description='Some description', category_id=self.category.id,
            guarantee=12, features={'feature_field': '2'}, price=399, is_active=True
        )
        self.storeproduct1 = StoreProduct.objects.create(
            product=self.product1, amount=10, store=self.store1
        )
        self.client.post(reverse('basket:basket_add'), {'productid': self.product1.id})
        self.client.login(username='User1', password='User1password')

    def test_basket_homepage(self):
        """
        Test homepage status code
        """
        response = self.client.get(reverse('basket:summary'))
        self.assertEqual(response.status_code, 200)

    def test_basket_homepage_context(self):
        """
        Test validates context on the homepage
        """
        response = self.client.get(reverse('basket:summary'))
        context = list(response.context['Products'])
        self.assertEqual(context, [{
            'amount': 1,
            'product': self.product1,
            'total_amount': 10,
            'total': 399
        }])

    def test_basket_homepage_context_on_lack_of_product(self):
        """
        Test validates context on the homepage on lack of product
        """
        self.storeproduct1.amount = 0
        self.storeproduct1.save()
        response = self.client.get(reverse('basket:summary'))

        context = list(response.context['Products'])

        self.assertEqual(context, [{
            'amount': 0,
            'product': self.product1,
            'total_amount': 0,
            'total': 0
        }])

    def test_basket_add(self):
        """
        Test adding item to the basket
        """
        response = self.client.post(reverse('basket:basket_add'), {'productid': self.product1.id})
        basket = Basket(response.wsgi_request)
        self.assertEqual(basket._basket, {str(self.product1.id): {'amount': 2}})

    def test_basket_patch_with_agreement(self):
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
        basket = Basket(response.wsgi_request)
        self.assertEqual(basket._basket, {str(self.product1.id): {'amount': 9}})

    def test_basket_patch_with_no_agreement(self):
        """
        Test updating item in the basket with requested amount greater than actual amount
        """
        data = {
            "product_id": self.product1.id,
            "product_amount": 20,
            "total_price": self.product1.price,
        }
        data_json = json.dumps(data)
        response = self.client.patch(reverse('basket:basket_update'), data_json)
        self.assertEqual(response.json(), {
            'agreement': False,
            'amount': 1,
        })
        basket = Basket(response.wsgi_request)
        self.assertEqual(basket._basket, {str(self.product1.id): {'amount': 1}})

    def test_basket_patch_with_no_agreement_minus(self):
        """
        Test updating item in the basket with requested amount less then 0
        """
        data = {
            "product_id": self.product1.id,
            "product_amount": -1,
            "total_price": self.product1.price,
        }
        data_json = json.dumps(data)
        response3 = self.client.patch(reverse('basket:basket_update'), data_json)
        self.assertEqual(response3.json(), {
            'agreement': False,
            'amount': 1,
        })
        basket = Basket(response3.wsgi_request)
        self.assertEqual(basket._basket, {str(self.product1.id): {'amount': 1}})

    def test_basket_patch_with_lack_of_product(self):
        """
        Test updating item in the basket with its actual amount equals 0
        """

        self.storeproduct1.amount = 0
        self.storeproduct1.save()

        data = {
            "product_id": self.product1.id,
            "product_amount": 9,
            "total_price": self.product1.price,
        }
        data_json = json.dumps(data)
        response3 = self.client.patch(reverse('basket:basket_update'), data_json)
        self.assertEqual(response3.json(), {
            'agreement': 'Out of stock'
        })
        basket = Basket(response3.wsgi_request)
        self.assertEqual(basket._basket, {str(self.product1.id): {'amount': 0}})

    def test_basket_delete(self):
        """
        Test deleting item from the basket
        """
        data = {
            'product_id': self.product1.id,
            'total_price': self.product1.price,
        }
        data_json = json.dumps(data)
        response = self.client.delete(reverse('basket:basket_update'), data_json)
        self.assertEqual(response.json(), {'total': '0', })
        basket = Basket(response.wsgi_request)
        self.assertEqual(basket._basket, {})


class TestBasketCheckout(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user('User1', 'email2@mail.com', 'User1password')
        self.category = InnerCategory.objects.create(
            name='Category', slug='Category', features=None
        )
        self.store1 = Store.objects.create(
            name='SomeStore', location='SomeWhere'
        )
        self.store2 = Store.objects.create(
            name='SomeStore2', location='SomeWhere2'
        )
        self.store3 = Store.objects.create(
            name='SomeStore3', location='SomeWhere3'
        )
        self.product1 = Product.objects.create(
            name='product1', slug='product1', description='Some description', category_id=self.category.id,
            guarantee=12, features={'feature_field': '2'}, price=399, is_active=True
        )
        self.storeproduct1 = StoreProduct.objects.create(
            product=self.product1, amount=10, store=self.store1
        )
        self.client.post(reverse('basket:basket_add'), {'productid': self.product1.id})
        self.client.login(username='User1', password='User1password')

        class BasketHandler():

            def set_basket_amount(amount, product_id):
                data = {
                    "product_id": product_id,
                    "product_amount": amount,
                    "total_price": 100,
                }
                data_json = json.dumps(data)
                self.client.patch(reverse('basket:basket_update'), data_json)

        self.basket_handler = BasketHandler

    def test_basket_checkout_one_to_one_ratio(self):
        """
        Test checkout on one-to-one ratio
        """
        self.basket_handler.set_basket_amount(10, self.product1.id)

        self.client.get(reverse('basket:checkout', kwargs={'store': self.store1.name}))

        orders_amount = OrderStore.objects.filter(storeproduct__product__id=self.product1.id).count()
        self.assertEqual(orders_amount, 1)
        orderstore = OrderStore.objects.get(storeproduct__product__id=self.product1.id)
        self.assertEqual(orderstore.amount, 10)
        order_product = OrderProduct.objects.filter(product__id=self.product1.id).count()
        self.assertEqual(order_product, 1)
        order = Order.objects.filter(products__id=self.product1.id).exists()
        self.assertEqual(order, True)

    def test_basket_checkout_two_store(self):
        """
        Test checkout with more then 1 store
        """
        StoreProduct.objects.create(
            product=self.product1, amount=6, store=self.store2
        )
        self.basket_handler.set_basket_amount(13, self.product1.id)

        self.client.get(reverse('basket:checkout', kwargs={'store': self.store1.name}))

        orders_amount = OrderStore.objects.filter(storeproduct__product__id=self.product1.id).count()
        self.assertEqual(orders_amount, 2)
        orders = OrderStore.objects.filter(storeproduct__product__id=self.product1.id)
        self.assertEqual(sum([item.amount for item in orders]), 13)
        order_product = OrderProduct.objects.filter(product__id=self.product1.id).count()
        self.assertEqual(order_product, 1)
        order = Order.objects.filter(products__id=self.product1.id).exists()
        self.assertEqual(order, True)

    def test_basket_checkout_on_lack_of_product(self):
        """
        Test checkout on lack of product on store
        """
        self.storeproduct1.amount = 0
        self.storeproduct1.save()
        self.basket_handler.set_basket_amount(13, self.product1.id)

        self.client.get(reverse('basket:checkout', kwargs={'store': self.store1.name}))

        order_store = OrderStore.objects.filter(storeproduct__product__id=self.product1.id).exists()
        self.assertEqual(order_store, 0)
        order = Order.objects.filter(products__id=self.product1.id).exists()
        self.assertEqual(order, False)
        order_product = OrderProduct.objects.filter(product__id=self.product1.id).exists()
        self.assertEqual(order_product, False)

    def test_basket_checkout_on_more_than_two_stores(self):
        """
        Test checkout on more than two stores
        """
        StoreProduct.objects.create(
            product=self.product1, amount=6, store=self.store2
        )
        StoreProduct.objects.create(
            product=self.product1, amount=7, store=self.store3
        )
        self.basket_handler.set_basket_amount(23, self.product1.id)

        self.client.get(reverse('basket:checkout', kwargs={'store': self.store1.name}))

        orders_amount = OrderStore.objects.filter(storeproduct__product__id=self.product1.id).count()
        self.assertEqual(orders_amount, 3)
        orders = OrderStore.objects.filter(storeproduct__product__id=self.product1.id)
        self.assertEqual(sum([item.amount for item in orders]), 23)
        order_product = OrderProduct.objects.filter(product__id=self.product1.id).count()
        self.assertEqual(order_product, 1)
        order = Order.objects.filter(products__id=self.product1.id).exists()
        self.assertEqual(order, True)

    def test_basket_checkout_on_empty_store_skipping(self):
        """
        Test checkout behavior on empty store
        """
        StoreProduct.objects.create(
            product=self.product1, amount=0, store=self.store2
        )
        self.basket_handler.set_basket_amount(10, self.product1.id)

        self.client.get(reverse('basket:checkout', kwargs={'store': self.store1.name}))

        orders_amount = OrderStore.objects.filter(storeproduct__product__id=self.product1.id).count()
        self.assertEqual(orders_amount, 1)
        orderstore = OrderStore.objects.get(storeproduct__product__id=self.product1.id)
        self.assertEqual(orderstore.amount, 10)
        order_product = OrderProduct.objects.filter(product__id=self.product1.id).count()
        self.assertEqual(order_product, 1)
        order = Order.objects.filter(products__id=self.product1.id).exists()
        self.assertEqual(order, True)
