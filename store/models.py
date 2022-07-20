from django.db import models
from django.urls import reverse

from mptt.models import TreeForeignKey, MPTTModel


class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)


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

    def get_absolute_url(self):
        return reverse('store:category', args=[self.slug])


class InnerCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    slug = models.SlugField(unique=True)
    features = models.JSONField(null=True,
                                blank=True,
                                help_text='features used for filter purpose'
    )

    class Meta:
        verbose_name_plural = 'Categories_inner'

    def __str__(self):
        return self.name

    def get_absolute_url(self,filters='start'):
        return reverse('store:product_list', args=[self.slug, filters])

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, sort=True):
        features = self.features

        if features == None:
            features = {}
        if 'fields' not in features:
            features['fields'] = {}
        if 'requested_fields' not in features:
            features['requested_fields'] = []
        for key in features['requested_fields']:
            if key not in features['fields']:
                features['fields'][key] = []
        for key in features['fields'].copy():
            if key not in features['requested_fields']:
                del features['fields'][key]
        if sort:
            for key in features['fields'].keys():
                features['fields'][key] = sorted(features['fields'][key])
        self.features = features
        super().save(force_insert, force_update, using, update_fields)


class Store(models.Model):
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = 'Locations'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=70)
    category = models.ForeignKey(InnerCategory, null=True, on_delete=models.SET_NULL)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=300)
    guarantee = models.IntegerField()
    features = models.JSONField(null=True,
                                blank=True,
                                help_text='Additional information for different Categories')
    price = models.IntegerField(null=False, blank=False, help_text='Current price for this item')
    is_active = models.BooleanField(default=False)
    availability = models.ManyToManyField(Store, through='StoreProduct')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    products = ProductManager()

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-is_active', '-name', '-created')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if self.features:
            category = InnerCategory.objects.get(id=self.category.id)
            category_features = category.features
            requested_fields = category.features['requested_fields']

            for key, item in self.features.items():
                if key not in requested_fields:
                    continue
                if key not in category_features['fields']:
                    category_features['fields'][key] = [item]
                    category.save()
                    continue
                if item in category_features['fields'][key]:
                    continue
                category_features['fields'][key].append(item)
                category.save()
    
        return super().save(force_insert, force_update, using, update_fields)


class StoreProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Amount table'


class PriceStory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price_tag = models.IntegerField(help_text='Outdated price for comparison')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Prices'
        ordering = ('product', '-date')

    def __str__(self):
        return str(self.product)