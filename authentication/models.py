from django.contrib.auth.models import AbstractUser
from django.db import models
from store.models import StoreProduct, Product

from .custom.constants import RATINGS


class CustomUser(AbstractUser):
    pass


class Review(models.Model):
    user = models.ForeignKey(
        CustomUser,
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review_pros = models.TextField(max_length=150, blank=True, null=True)
    review_cons = models.TextField(max_length=150, blank=True, null=True)
    review_commentary = models.TextField(max_length=150, blank=True, null=True)
    rating = models.IntegerField(choices=RATINGS)
    pub_date = models.DateTimeField(auto_now_add=True)

    class META:
        unique_together = ['product', 'user']
    
    def __str__(self):
        return f'Review on {self.product} written by {self.user}'


class Order(models.Model):
    user = models.ForeignKey(
        CustomUser,
        blank=False,
        null=True,
        on_delete=models.SET_NULL
    )
    products = models.ManyToManyField(Product, through='OrderProduct')
    store = models.ManyToManyField(StoreProduct, through='OrderStore')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order № {self.id}"

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)


class OrderStore(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    storeproduct = models.ForeignKey(StoreProduct, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)