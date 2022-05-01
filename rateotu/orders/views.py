from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from rateotu.accounts.permissions import IsCustomer, IsEmployee
from rateotu.orders.serializers import (
    OrderListSerializer,
    OrderCreateSerializer,
    OrderItemSerializer,
)
from rateotu.orders.models import Order, OrderItem
from rateotu.orders.services import (
    create_customer_order,
)
from rateotu.orders.filters import OrderItemFilter
from rateotu.utils.api import ReadWriteSerializerMixin


# Order Collection controller
class OrderListCreateView(ReadWriteSerializerMixin, generics.ListCreateAPIView):
    """
    List all orders that are owned by an authenticated
    customer user, or create a new order.
    """

    read_serializer_class = OrderListSerializer
    write_serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated & (IsCustomer | IsEmployee)]

    def get_queryset(self):
        return (
            Order.objects.owned_by_user(self.request.user.customer)
            .prefetch_related("order_items__item__category")
            .select_related("customer__user")
            .order_by("-id")
        )

    # This 'hook' runs after the 'serializer.is_valid(raise_exception=True)'
    # Which means the 'serializer.validated_data' will be populated with a
    # validated data.
    def perform_create(self, serializer):
        validated_data = serializer.validated_data.copy()
        total = validated_data.pop("total")
        order_items = validated_data.pop("order_items")
        create_customer_order(self.request.user.customer, total, order_items)


class OrderItemListView(generics.ListAPIView):
    """
    List all order items.
    """

    permission_classes = [IsAuthenticated & IsEmployee]
    serializer_class = OrderItemSerializer
    filterset_class = OrderItemFilter

    def get_queryset(self):
        return OrderItem.objects.select_related(
            "order", "item__category", "customer__user"
        ).order_by("-id")
