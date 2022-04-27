from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from rateotu.accounts.permissions import IsCustomer, IsEmployee
from rest_framework.permissions import SAFE_METHODS
from rateotu.orders.serializers import OrderListSerializer, OrderCreateSerializer
from rateotu.orders.models import Order
from rateotu.orders.services import create_customer_order


# NOTE: Order Collection controller
# NOTE: Only HEAD, OPTIONS, GET, POST http methods
class OrderListCreateView(generics.ListCreateAPIView):
    """
    List all orders that are owned by the authenticated
    customer user, or create a new order.
    """

    serializer_classes = {"read": OrderListSerializer, "write": OrderCreateSerializer}
    permission_classes = [IsAuthenticated & (IsCustomer | IsEmployee)]

    def get_queryset(self):
        return (
            Order.objects.owned_by_user(self.request.user.customer)
            .prefetch_related("order_items")
            .select_related("customer__user")
            .order_by("id")
        )

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return self.serializer_classes["read"]
        return self.serializer_classes["write"]

    def perform_create(self, serializer):
        # NOTE: This 'hook' runs after the 'serializer.is_valid(raise_exception=True)'
        # Which means the 'serializer.data' will be populated with a validated data
        create_customer_order(self.request.user, serializer.data)
