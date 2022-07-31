from django.db.models import Count, Q, Avg


def get_annotated_products(products_queryset):
    """
    Annotates products query
    """

    # Note: annotating more than one aggregate prohibited
    # but can work in some cases with distinct = True

    stores_with_stock = Count('storeproduct', filter=Q(storeproduct__amount__gt=0), distinct=True)
    avg_rating = Avg('review__rating')
    annotated_stores_queryset = products_queryset.annotate(
        avg_rating=avg_rating,
        number_of_shops=stores_with_stock,
    )
    return annotated_stores_queryset
