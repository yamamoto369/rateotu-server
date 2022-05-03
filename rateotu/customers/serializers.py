from rest_framework import serializers

from rateotu.customers.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Customer
        fields = ["id", "username"]
