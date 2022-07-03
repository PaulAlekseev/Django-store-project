from django.db import models

from mptt.models import TreeForeignKey, MPTTModel


class Category(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey('self',
                            blank=True,
                            null=True,
                            on_delete=models.SET_NULL,
                            related_name='Category',
                            verbose_name='Categories')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = 'Locations'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=70)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=300)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    guarantee = models.IntegerField()
    core = models.CharField(max_length=50)
    socket = models.CharField(max_length=50)
    total_cores = models.IntegerField()
    total_threads = models.IntegerField()
    frequency = models.DecimalField(max_digits=2, decimal_places=1)
    cache = models.IntegerField()
    bus_speed = models.IntegerField()
    availability = models.ManyToManyField(Store, through='StoreProduct')

    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name


class StoreProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = 'Amount table'


class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price_tag = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Prices'

    def __str__(self):
        return str(self.price_tag) + ' ' + str(self.date)




