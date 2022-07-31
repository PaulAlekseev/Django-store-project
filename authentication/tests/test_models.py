from django.test import TestCase

from authentication.models import Review, CustomUser
from store.models import Product, InnerCategory


class TestAuthenticationModels(TestCase):

    def test_review_string_method(self):
        user = CustomUser.objects.create(
            username='Name', email='User1@mail.ru',
            is_active=True
        )
        category = InnerCategory.objects.create(
            name='Category', slug='Category', features=None
        )
        product = Product.objects.create(
            name='product1', slug='product1', description='Some description', category=category,
            guarantee=12, features={'feature_field': '2'}, price=399, is_active=True
        )
        review = Review.objects.create(
            user=user, rating=3, product=product
        )

        review_string = str(review)
        
        self.assertEqual(review_string, f'Review on {product} written by {user}')