from urllib import response
from django.db.models import Count, Q
from django.http import JsonResponse
from django.views import generic

from .models import Category, InnerCategory, Product
from .custom.handlers.string_handlers import envelop
from .custom.handlers.query_handlers import query_to_json
from .custom.annotations import get_annotated_category

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
    template_name = 'store/product_list.html'
    context_object_name = 'Products'

    def get_queryset(self):
        queryset = Product.products.filter(
            category__slug=self.kwargs['category_slug']
            )
        queryset = get_annotated_category(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Category'] = InnerCategory.objects.get(slug=self.kwargs['category_slug'])
        context['slug'] = self.kwargs['category_slug']
        return context

    def post(self, request, slug):
        data = json.loads(request.body)
        if data:
            extra_filter = " AND ".join([
                f"store_product.features -> '{key}' IN {envelop(value[0]) if len(value) == 1 else tuple(value)}" for key, value in data.items()
                ])
            query = Product.objects.filter(category__slug=slug).extra(
                where=[extra_filter]
                )
        else:
            query = Product.products.filter(
            category__slug=slug
            )

        query = get_annotated_category(query)
        response = JsonResponse(query_to_json(query))
        return response


class ProductDetailView(generic.detail.DetailView):
    template_name = 'store/product_details.html'
    model = Product
    context_object_name = 'Product'
