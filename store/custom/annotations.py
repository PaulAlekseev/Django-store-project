from django.db.models import Count, Q


def get_annotated_products(products_queryset):
    stores_with_stock = Count('storeproduct', filter=Q(storeproduct__amount__gt=0))
    annotated_stores_queryset = products_queryset.annotate(
        number_of_shops=stores_with_stock,
    )
    return annotated_stores_queryset
