from django.db.models import Count, Q
from django.http import HttpResponse
from .models import Category, InnerCategory, Product
from django.views import generic

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
            category__slug=self.kwargs['category_slug']).annotate(
            number_of_shops=Count('storeproduct', filter=Q(storeproduct__amount__gt=0)))
        bruh = Product.objects.filter(features__bruh__in=[2, 3], features__nobruh__in=[4])
        print(bruh)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Category'] = InnerCategory.objects.get(slug=self.kwargs['category_slug'])
        context['slug'] = self.kwargs['category_slug']
        return context

    def post(self, request, slug):
        data = json.loads(request.body)
        print(data)
        query = Product.objects.extra(where=["('store_product' -> 'features' -> 'bruh') IN ('2', '3') AND ('store_product' -> 'features' -> 'nobruh') IN ('4')"])
        print(query)
        return HttpResponse('1')


class ProductDetailView(generic.detail.DetailView):
    template_name = 'store/product_details.html'
    model = Product
    context_object_name = 'Product'
