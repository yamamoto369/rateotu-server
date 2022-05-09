from rest_framework import serializers

from rateotu.customers.serializers import CustomerSerializer
from rateotu.tables.models import Seat, Table


class TableNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = [
            "id",
            "table_number",
        ]


class SeatReadSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    table = TableNestedSerializer()

    class Meta:
        model = Seat
        fields = ["id", "is_occupied", "table", "customer"]


class SeatWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ["is_occupied"]


class TableSerializer(serializers.ModelSerializer):
    seats = SeatReadSerializer(many=True)
    available_seat_capacity = serializers.ReadOnlyField()

    class Meta:
        model = Table
        fields = "__all__"
