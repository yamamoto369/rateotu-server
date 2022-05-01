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


class OrderItemBulkUpdateWriteSerializer(serializers.Serializer):
    order_item_ids = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=False
    )
    order_status = serializers.ChoiceField(OrderItem.ORDER_STATUS_CHOICES)

    def validate_order_item_ids(self, value):
        """
        Checks that 'order_item_ids' belong to a valid OrderItem instances.
        """
        not_valid_ids = []
        qs_ids = OrderItem.objects.filter(id__in=value).values_list("id", flat=True)
        # Working over 1 query (qs now evaluated, now in memory)
        for order_item_id in value:
            if order_item_id not in qs_ids:
                not_valid_ids.append(order_item_id)
        if not_valid_ids:
            msg = (
                f"{not_valid_ids} are not a valid ids!"
                if len(not_valid_ids) > 1
                else f"{not_valid_ids[0]} is not a valid id!"
            )
            raise serializers.ValidationError(msg)
        return value
