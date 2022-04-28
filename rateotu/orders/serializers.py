from rest_framework import serializers

from rateotu.menus.serializers import ItemReadSerializer, ItemWriteSerializer
from rateotu.customers.serializers import CustomerSerializer
from rateotu.orders.models import Order, OrderItem


class OrderItemReadSerializer(serializers.ModelSerializer):
    item = ItemReadSerializer()

    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderListSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    order_items = OrderItemReadSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"


class OrderCreateSerializer(serializers.ModelSerializer):
    order_items = serializers.ListField(child=ItemWriteSerializer(), allow_empty=False)

    class Meta:
        model = Order
        # NOTE: All which are required except the customer (check views)
        exclude = ["customer"]


class OrderReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemReadSerializer()
    customer = CustomerSerializer()
    order = OrderReadSerializer()

    class Meta:
        model = OrderItem
        fields = "__all__"
