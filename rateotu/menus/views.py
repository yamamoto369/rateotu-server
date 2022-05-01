from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from rateotu.menus.serializers import MenuSerializer
from rateotu.menus.models import Menu
from rateotu.accounts.permissions import IsCustomer, IsEmployee


class MenuListView(generics.ListAPIView):
    """
    Get a list of all menus (including menu items).
    """

    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated & (IsCustomer | IsEmployee)]

    def get_queryset(self):
        return Menu.objects.prefetch_related(
            "items__category"
        )  # 2 queries instead N+1
