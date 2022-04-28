from django_filters import rest_framework as filters
from rateotu.orders.models import OrderItem


class OrderItemFilter(filters.FilterSet):
    item_category = filters.CharFilter(
        field_name="item__category__name",
        lookup_expr="exact",
        distinct=True,
    )

    class Meta:
        model = OrderItem
        fields = ["item_category"]
