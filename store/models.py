from django.db import models
from django.urls import reverse

from mptt.models import TreeForeignKey, MPTTModel


class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)


class Category(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='Category',
        verbose_name='Categories'
    )
    image = models.ImageField(
        upload_to='images/categories',
        null=False,
        blank=False,
        default='images/categories/default.png',
    )
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:category', args=[self.slug])


class InnerCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL
    )
    image = models.ImageField(
        upload_to='images/categories',
        null=False,
        blank=False,
        default='images/categories/default.png',
    )
    slug = models.SlugField(unique=True)
    features = models.JSONField(
        null=True,
        blank=True,
        help_text='features used for filter purpose'
    )

    class Meta:
        verbose_name_plural = 'Categories_inner'

    def __str__(self):
        return self.name

    def get_absolute_url(self, filters=''):
        return reverse('store:filtered_product_list', args=[self.slug, filters])

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, sort=True):
        features = self.features

        # Converts features to correct format
        if features == None:
            features = {}
        if 'fields' not in features:
            features['fields'] = {}
        if 'requested_fields' not in features:
            features['requested_fields'] = []

        # Syncronizes requested fields with fields
        products = Product.objects.filter(
            category__id=self.id
        )
        for key in features['requested_fields']:
            if key not in features['fields']:
                features['fields'][key] = []
                features['fields'][key] = list(set([item.get_feature(key) for item in products]))
                if None in features['fields'][key]:
                    features['fields'][key].remove(None)

        for key in features['fields'].copy():
            if key not in features['requested_fields']:
                del features['fields'][key]

        # Sorts features for better view in filters
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
    image = models.ImageField(
        upload_to='images/products',
        null=False,
        blank=False,
        default='images/products/default.png',
    )
    description = models.TextField(max_length=300)
    guarantee = models.IntegerField()
    features = models.JSONField(
        null=True,
        blank=True,
        help_text='Additional information for different Categories'
    )
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

            self.features = {key: str(item) for key, item in self.features.items()}

            for key, item in self.features.items():
                string_item = str(item)
                if key not in requested_fields:
                    continue
                if key not in category_features['fields']:
                    category_features['fields'][key] = [string_item]
                    category.save()
                    continue
                if string_item in category_features['fields'][key]:
                    continue
                category_features['fields'][key].append(string_item)
                category.save()
    
        return super().save(force_insert, force_update, using, update_fields)

    def get_feature(self, feature_key):
        if not self.features:
            return None
        if feature_key in self.features:
            return self.features[feature_key]



class StoreProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Amount table'

    def __str__(self):
        return self.product.name + ' from ' + self.store.name
