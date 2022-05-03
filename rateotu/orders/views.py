from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rateotu.accounts.permissions import IsCustomer, IsEmployee
from rateotu.orders.serializers import (
    OrderListSerializer,
    OrderCreateSerializer,
    OrderItemSerializer,
    OrderItemBulkUpdateWriteSerializer,
)
from rateotu.orders.models import Order, OrderItem
from rateotu.orders.services import (
    create_customer_order,
    bulk_update_order_items_order_status,
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


class OrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific order item.
    """

    lookup_field = "pk"
    permission_classes = [IsAuthenticated & IsEmployee]
    serializer_class = OrderItemSerializer

    # Gets a object intance based on the qs bellow
    # obj = get_object_or_404(queryset, **filter_kwargs)
    def get_queryset(self):
        return OrderItem.objects.select_related(
            "order", "item__category", "customer__user"
        )


# There are a many different ways to do bulk updates or creates over a REST API!
# Many companies do it in a different ways, I decided to "follow" the ZenDesk's API way
# (one batch URL endpoint per resource, for both bulk updates or creates).
# READ: https://www.codementor.io/blog/batch-endpoints-6olbjay1hd
# The code bellow can be customized to allow bulk creates as well.
class OrderItemBulkUpdateView(APIView):
    """
    Bulk update order status for a multiple order items
    or just a specific one.
    """

    http_method_names = [
        "patch",
        "head",
        "options",
    ]
    permission_classes = [IsAuthenticated & IsEmployee]
    read_serializer_class = OrderItemSerializer
    write_serializer_class = OrderItemBulkUpdateWriteSerializer

    # Patch method because we do a partial bulk updates over resources (objs) in a qs.
    def patch(self, request, *args, **kwargs):
        write_serializer = self.write_serializer_class(data=request.data)
        # Raises the 'ValidationError' exception and returns
        # a http400 response if the supplied data was invalid.
        write_serializer.is_valid(raise_exception=True)
        validated_data = write_serializer.validated_data.copy()
        order_item_ids = validated_data.get("order_item_ids")
        order_status = validated_data.get("order_status")
        bulk_update_order_items_order_status(order_item_ids, order_status)
        updated_order_items = OrderItem.objects.filter(
            id__in=order_item_ids, order_status=order_status
        )
        # Serializing response output
        read_serializer = self.read_serializer_class(updated_order_items, many=True)
        return Response(data=read_serializer.data, status=status.HTTP_200_OK)
