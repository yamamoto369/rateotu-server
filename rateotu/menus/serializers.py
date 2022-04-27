from rest_framework import serializers

from rateotu.menus.models import Category, Item, Menu


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ItemReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Item
        fields = "__all__"


class ItemWriteSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField()
    id = serializers.IntegerField()

    class Meta:
        model = Item
        exclude = ["category"]


class MenuSerializer(serializers.ModelSerializer):
    items = ItemReadSerializer(many=True)

    class Meta:
        model = Menu
        fields = "__all__"
        ready_only_fields = ["items"]
