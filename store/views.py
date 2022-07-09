from django.shortcuts import get_object_or_404
from django.db.models import Count, Q, Subquery, F, Prefetch
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


class ProductListView(generic.list.ListView):
    template_name = 'store/productList.html'
    context_object_name = 'Products'

    def get_queryset(self):
        queryset = Product.products.filter(
            category__slug=self.kwargs['category_slug']).annotate(
            number_of_shops=Count('storeproduct', filter=Q(storeproduct__amount__gt=0)))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Category'] = InnerCategory.objects.get(slug=self.kwargs['category_slug'])
        return context

