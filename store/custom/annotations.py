from django.db.models import Count, Q, Sum


def get_annotated_products(products_queryset):
    stores_with_stock = Count('storeproduct', filter=Q(storeproduct__amount__gt=0))
    total_amount = Sum('storeproduct__amount')
    annotated_stores_queryset = products_queryset.annotate(
        number_of_shops=stores_with_stock,
        total_amount=total_amount,
    )
    return annotated_stores_queryset
