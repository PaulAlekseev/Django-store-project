from base64 import urlsafe_b64encode
from itertools import product
from unicodedata import category
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str

from store.models import Product, InnerCategory
from authentication.tokens import account_activation_token
from authentication.models import CustomUser, Review, Order, OrderProduct


class TestAuthenticationRegistrationViews(TestCase):

    def test_registration_redirection_on_succes(self):
        """
        Test for redirection on succes
        """
        form_data = {
            'username': 'User1',
            'email': 'User1@mail.ru',
            'password1': 'pASs12345678',
            'password2': 'pASs12345678'
        }
        response = self.client.post(reverse('authentication:registration'), form_data)

        self.assertEqual(response.status_code, 302)

    def test_registration_on_invalid_data(self):
        """
        Test registration on invalid data
        """
        form_data = {
            'username': 'User1',
            'email': 'User1@mail.ru',
            'password1': 'pASs123',
            'password2': 'pASs123'
        }
        response = self.client.post(reverse('authentication:registration'), form_data)

        user = CustomUser.objects.filter(username='User1')
        self.assertFalse(user.exists())
        self.assertNotEqual(response.status_code, 302)

    def test_user_activation_view(self):
        """
        Test user activation after account registration
        """
        user = CustomUser.objects.create(
            username='User1', email='User1@mail.ru', is_active=False
        )
        uid = urlsafe_b64encode(force_bytes(user.pk)),
        token = account_activation_token.make_token(user=user)
        
        response = self.client.get(reverse('authentication:activation', kwargs={
            'uidb64': force_str(uid[0])[:2], 'token': token
        }))

        self.assertEqual(response.status_code, 302)
        user1 = CustomUser.objects.get(username='User1')
        self.assertTrue(user1.is_active)

    def test_invalid_activation_view(self):
        """
        Test if user activation works with invalid information
        """
        user = CustomUser.objects.create(
            username='User1', email='User1@mail.ru', is_active=False
        )
        uid = urlsafe_b64encode(force_bytes(user.pk)),
        
        response = self.client.get(reverse('authentication:activation', kwargs={
            'uidb64': force_str(uid[0])[:2], 'token': 'b9eqeb-85a7fe5cd1d0abd39b7fc5ee77fc6e01'
        }))

        self.assertEqual(response.status_code, 200)


class TestauthenticationLoginRequiredViews(TestCase):

    def setUp(self):
        self.category = InnerCategory.objects.create(
            name='Category', slug='Category', features=None
        )
        self.product = Product.objects.create(
            name='product1', slug='product1', description='Some description', category_id=self.category.id,
            guarantee=12, features={'feature_field': '2'}, price=399, is_active=True
        )
        self.user = CustomUser.objects.create(
            username='Name', email='User1@mail.ru',
            is_active=True
        )
        self.user.set_password('User1password')
        self.user.save()
        Review.objects.create(
            user=self.user, product=self.product, rating=2
        )
        self.inner_category = InnerCategory.objects.create(
            name='InnerCategory', slug='InnerCategory',
            features=None
        )
        self.order = Order.objects.create(
            user=self.user
        )
        OrderProduct.objects.create(
            order=self.order, product=self.product, amount=4
        )
        OrderProduct.objects.create(
            order=self.order, product=self.product, amount=2
        )
        self.client.login(username='Name', password='User1password')

    def test_profile_review_url(self):
        """
        Test if profile review is accessible
        """
        response = self.client.get(reverse('authentication:reviews'))

        reviews = Review.objects.filter(user__id=self.user.id)

        self.assertEqual(list(response.context['Reviews']), list(reviews))
        self.assertEqual(response.status_code, 200)

    def test_profile_init_url(self):
        """
        Test if profile is accessible
        """
        response = self.client.get(reverse('authentication:profile'))

        order = Order.objects.filter(user__id=self.user.id)

        self.assertEqual(list(response.context['Orders']), list(order))
        self.assertEqual(response.status_code, 200)


class TestAuthenticationReviewViews(TestCase):
    
    def setUp(self):
        self.category = InnerCategory.objects.create(
            name='Category', slug='Category', features=None
        )
        self.user = CustomUser.objects.create(
            username='Name', email='User1@mail.ru',
            is_active=True
        )
        self.product = Product.objects.create(
            name='product1', slug='product1', description='Some description', category=self.category,
            guarantee=12, features={'feature_field': '2'}, price=399, is_active=True
        )
        self.user.set_password('User1password')
        self.user.save()
        self.client.login(username='Name', password='User1password')
        
    def test_if_review_create_accessible(self):
        """
        Test if review create is accessible
        """
        response = self.client.get(reverse('authentication:create_review', kwargs={'slug': self.product.slug}))

        self.assertEqual(response.status_code, 200)

    def test_review_create_redirection_on_success(self):
        """
        Test for redurection on success
        """
        form_data = {
            'user': self.user,
            'rating': 2,
        }
        response = self.client.post(reverse('authentication:create_review', kwargs={'slug': self.product.slug}), form_data)

        self.assertEqual(response.status_code, 302)
    
    def test_review_create_on_invalid_data(self):
        """
        Test for invalid data on review create
        """
        form_data = {
            'user': self.user,
            'rating': 6,
        }
        response = self.client.post(reverse('authentication:create_review', kwargs={'slug': self.product.slug}), form_data)

        self.assertEqual(response.status_code, 200)

    def test_on_a_user_already_reviewed(self):
        """
        Test for second review on same product
        """
        Review.objects.create(
            user=self.user, rating=3, product=self.product
        )
        response = self.client.get(reverse('authentication:create_review', kwargs={'slug': self.product.slug}))

        self.assertEqual(response.status_code, 302)

    def test_review_update_redirection_on_success(self):
        """
        Test for redurection on success
        """
        review = Review.objects.create(
            user=self.user, rating=3, product=self.product
        )
        form_data = {
            'user': self.user,
            'rating': 2,
        }
        response = self.client.post(reverse('authentication:update_review', kwargs={'id': review.id}), form_data)

        self.assertEqual(response.status_code, 302)
    
    def test_review_update_on_invalid_data(self):
        """
        Test for invalid data on review update
        """
        review = Review.objects.create(
            user=self.user, rating=3, product=self.product
        )
        form_data = {
            'user': self.user,
            'rating': 6,
        }
        response = self.client.post(reverse('authentication:update_review', kwargs={'id': review.id}), form_data)

        self.assertEqual(response.status_code, 200)

    def test_review_delete_redirection_on_success(self):
        """
        Test for redirection on success
        """
        review = Review.objects.create(
            user=self.user, rating=3, product=self.product
        )
        response = self.client.post(reverse('authentication:delete_review', kwargs={'id': review.id}))

        self.assertEqual(response.status_code, 302)
    
