from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from rateotu.accounts.permissions import IsCustomer, IsEmployee
from rest_framework.permissions import SAFE_METHODS
from rateotu.orders.serializers import (
    OrderListSerializer,
    OrderCreateSerializer,
    OrderItemSerializer,
)
from rateotu.orders.models import Order, OrderItem
from rateotu.orders.services import create_customer_order
from rateotu.orders.filters import OrderItemFilter


# NOTE: Order Collection controller
# NOTE: Only HEAD, OPTIONS, GET, POST http methods
class OrderListCreateView(generics.ListCreateAPIView):
    """
    List all orders that are owned by an authenticated
    customer user, or create a new order.
    """

    serializer_classes = {"read": OrderListSerializer, "write": OrderCreateSerializer}
    permission_classes = [IsAuthenticated & (IsCustomer | IsEmployee)]

    def get_queryset(self):
        return (
            Order.objects.owned_by_user(self.request.user.customer)
            .prefetch_related("order_items__item__category")
            .select_related("customer__user")
            .order_by("-id")
        )

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return self.serializer_classes["read"]
        return self.serializer_classes["write"]

    def perform_create(self, serializer):
        # NOTE: This 'hook' runs after the 'serializer.is_valid(raise_exception=True)'
        # Which means the 'serializer.validated_data' will be populated with a
        # validated data.
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
