from django.shortcuts import render, get_object_or_404
from .models import Category, InnerCategory


def index(request):
    categories = Category.objects.root_nodes()
    return render(request, 'store/index.html', {'categories': categories})


def category_list(request, category_slug):
    inners = InnerCategory.objects.filter(category__slug=category_slug)
    if len(inners) > 0:
        return render(request, 'store/category.html', {'categories': inners})
    categories = get_object_or_404(Category, slug=category_slug).get_descendants()

    return render(request, 'store/category.html', {'categories': categories})


def product_list(request, category_slug):
    pass
