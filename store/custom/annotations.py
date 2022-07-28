from django.db.models import Count, Q, Sum, Avg


def get_annotated_products(products_queryset):
    stores_with_stock = Count('storeproduct', filter=Q(storeproduct__amount__gt=0), distinct=True)
    total_amount = Sum('storeproduct__amount', distinct=True)
    avg_rating = Avg('review__rating', distinct=True)
    annotated_stores_queryset = products_queryset.annotate(
        avg_rating=avg_rating,
        number_of_shops=stores_with_stock,
        total_amount=total_amount,
    )
    return annotated_stores_queryset
