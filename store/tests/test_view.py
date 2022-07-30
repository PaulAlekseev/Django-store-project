from unicodedata import category
from urllib import response
from django.test import TestCase
from django.urls import reverse

from ..models import InnerCategory, Store, Product, StoreProduct, Category


class TestStoreView(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name='Category', slug='Category'
        )
        self.category1 = Category.objects.create(
            name='Category2', slug='Category2', parent=self.category
        )
        self.inner_category = InnerCategory.objects.create(
            name='InnerCategory', slug='InnerCategory',
            features=None, category=self.category1
        )
        self.store1 = Store.objects.create(
            name='SomeStore', location='SomeWhere'
        )
        self.product1 = Product.objects.create(
            name='product1', slug='product1', description='Some description', category_id=self.inner_category.id,
            guarantee=12, features={'feature1': '2', 'feature2': '4', 'feature3': '7'}, price=399, is_active=True
        )
        self.storeproduct1 = StoreProduct.objects.create(
            product=self.product1, amount=10, store=self.store1
        )

    def test_index_url(self):
        """
        Test index page on status code and context
        """
        response = self.client.get(reverse('store:index'))

        self.assertEqual(response.status_code, 200)
        categories = Category.objects.root_nodes()
        self.assertEqual(list(response.context['Categories']), list(categories))

    def test_category_list_view_on_outter_category(self):
        """
        Test category list on outter category
        """
        response = self.client.get(reverse('store:category', kwargs={'slug': self.category.slug}))

        self.assertEqual(response.status_code, 200)
        categories = Category.objects.filter(slug=self.category.slug).get_descendants()
        self.assertEqual(list(response.context['Categories']), list(categories))


    def test_category_list_view_on_inner_category(self):
        """
        Test category list on outter category
        """
        response = self.client.get(reverse('store:category', kwargs={'slug': self.category1.slug}))

        self.assertEqual(response.status_code, 200)
        categories = InnerCategory.objects.filter(category__slug=self.category1.slug)
        self.assertEqual(list(response.context['Categories']), list(categories))
        
    def test_product_list_view_on_initial_request(self):
        """
        Test product list on initial request without filters
        """
        response = self.client.get(reverse('store:filtered_product_list', kwargs={
            'category_slug': self.inner_category.slug, 'filters': ''
        }))

        self.assertEqual(response.status_code, 200)
        product_list = Product.products.filter(
            category__slug=self.inner_category.slug
        ).order_by('name')
        self.assertEqual(list(response.context['Products']), list(product_list))

    def test_product_list_view_on_filtered_request(self):
        """
        Test product list with filteres
        """
        filters = '?filters=feature1%252&search=product'
        response = self.client.get(reverse('store:filtered_product_list', kwargs={
            'category_slug': self.inner_category.slug, 'filters': ''
        }) + filters)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['Products'][0], self.product1)

    def test_product_list_view_on_invalid_filtered_request(self):
        """
        Test product list with invalid filteres
        """
        filters = '?filters=feature1%254'
        response = self.client.get(reverse('store:filtered_product_list', kwargs={
            'category_slug': self.inner_category.slug, 'filters': ''
        }) + filters)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['Products']), [])



    def test_product_detail_view(self):
        """
        Test product detail view
        """
        response = self.client.get(reverse('store:product_detail', kwargs={
            'slug': self.product1.slug
        }))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['Product'], self.product1)

    def test_search_list_view(self):
        """
        Test search list on request
        """
        response = self.client.get(reverse('store:search') + '?search_form=product')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['Products'])[0], self.product1)
        
    def test_search_list_view_invalid_input(self):
        """
        Test search list on invalid request
        """
        response = self.client.get(reverse('store:search') + '?search_form=noproduct')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['Products']), [])