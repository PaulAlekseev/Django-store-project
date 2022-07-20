from django.db.models import Count
from django.http import JsonResponse
from django.views import generic
from django.urls import reverse

from .models import Category, InnerCategory, Product
from .custom.handlers.string_handlers import envelop, JSON_to_string, string_to_JSON
from .custom.annotations import get_annotated_products

import json


class IndexCategoryView(generic.list.ListView):
    template_name = 'store/index.html'
    context_object_name = 'Categories'

    def get_queryset(self):
        context = Category.objects.root_nodes()
        return context.order_by('name')


class CategoryListView(generic.list.ListView):
    template_name = 'store/category.html'
    context_object_name = 'Categories'

    def get_queryset(self):
        inners = InnerCategory.objects.filter(category__slug=self.kwargs.get('slug'))
        if len(inners) > 0:
            return inners
        categories = Category.objects.get(slug=self.kwargs.get('slug')).get_descendants()
        return categories


class ProductListView(generic.list.ListView):
    paginate_by = 5
    template_name = 'store/product_list.html'
    context_object_name = 'Products'

    def get_queryset(self):
        filters = self.kwargs['filters']
        products = Product.products.filter(
            category__slug=self.kwargs['category_slug']
            ).order_by('name')

        if filters != 'start':
            data = string_to_JSON(filters)
            extra_filter = " AND ".join([
                f"store_product.features -> '{key}' IN {envelop(value[0]) if len(value) == 1 else tuple(value)}" for key, value in data.items()
                ])
            products = products.extra(
                where=[extra_filter]
                )

        queryset = get_annotated_products(products)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Category'] = InnerCategory.objects.annotate(
            amount=Count('product')
            ).get(slug=self.kwargs['category_slug'])
        context['slug'] = self.kwargs['category_slug']
        context['num_pages'] = context['Category'].amount
        return context

    def post(self, request, slug):
        data = json.loads(request.body)
        filters = JSON_to_string(data['checkboxes'])
        slug = data['category_slug']
        args = {
            'category_slug': slug,
            'filters': filters,
            }
        if filters == '':
            filters = 'start'
        hello = JsonResponse({'href': reverse('store:product_list', args=[slug, filters])})
        return hello


class ProductDetailView(generic.detail.DetailView):
    template_name = 'store/product_details.html'
    model = Product
    context_object_name = 'Product'
