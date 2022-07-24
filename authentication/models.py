from django.contrib.auth.models import AbstractUser
from django.db import models
from store.models import StoreProduct
from store.models import Store
from store.models import Product


class CustomUser(AbstractUser):
    pass


class Order(models.Model):
    products = models.ManyToManyField(Product, through='OrderProduct')
    store = models.ManyToManyField(StoreProduct, through='OrderStore')
    date = models.DateTimeField(auto_now_add=True)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)


class OrderStore(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    storeproduct = models.ForeignKey(StoreProduct, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)