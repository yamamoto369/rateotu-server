from django_filters import rest_framework as filters

from rateotu.orders.models import OrderItem


class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class OrderItemFilter(filters.FilterSet):
    item_category = filters.CharFilter(
        field_name="item__category__name",
        lookup_expr="exact",
        distinct=True,
    )
    order_status = CharInFilter(field_name="order_status", lookup_expr="in")

    class Meta:
        model = OrderItem
        fields = ["item_category", "order_status"]
