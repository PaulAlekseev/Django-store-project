from django.views import generic

from .models import Category, InnerCategory, Product
from .custom.handlers.string_handlers import string_to_dictionary
from .custom.handlers.product_former import product_former
from .custom.annotations import get_annotated_products
from authentication.models import Review
from .custom.constants import PRODUCTS_PER_PAGE


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
    paginate_by = PRODUCTS_PER_PAGE
    template_name = 'store/product_list.html'
    context_object_name = 'Products'

    def get_queryset(self):
        request_filters = self.request.GET
        products = Product.products.filter(
            category__slug=self.kwargs['category_slug']
            ).order_by('name')

        products = product_former.get_products(products, request_filters)

        queryset = get_annotated_products(products)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Category'] = InnerCategory.objects.get(slug=self.kwargs['category_slug'])
        context['slug'] = self.kwargs['category_slug']
        filters_string = self.request.GET.get('filters')
        filters = (string_to_dictionary(filters_string) if filters_string else None)
        context['checkboxes'] = (
            '~'.join([key+'-'+value for key, values in filters.items() for value in values]) if filters else []
            )
        context['search'] = (self.request.GET.get('search') or '')
        return context


class ProductDetailView(generic.detail.DetailView):
    template_name = 'store/product_details.html'
    model = Product
    context_object_name = 'Product'

    def get_object(self):
        obj = get_annotated_products(
            Product.objects.filter(slug=self.kwargs['slug'])
        )[0]

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['Reviews'] = Review.objects.filter(
            product__slug=self.kwargs['slug']
        ).select_related(
            'user'
        )
        return context


class SearchListView(generic.list.ListView):
    paginate_by = PRODUCTS_PER_PAGE
    template_name = 'store/search_product.html'
    context_object_name = 'Products'

    def get_queryset(self):
        search_for = self.request.GET.get('search_form')
        query = get_annotated_products(Product.products.filter(name__icontains=search_for).select_related(
            'category'
            ).order_by('-category'))
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Categories'] = list(dict.fromkeys([category.category for category in context['Products']]))
        context['search'] = self.request.GET.get('search_form'),
        return context
