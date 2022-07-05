from django.shortcuts import render, get_object_or_404, HttpResponse
from django.db.models import Max, Exists
from .models import Category, InnerCategory, Product, PriceStory
from django.views import generic


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
        categories = get_object_or_404(Category, slug=self.kwargs.get('slug')).get_descendants()
        return categories


# def product_list(request, category_slug):
#     products = Product.products.filter(category__slug=category_slug)