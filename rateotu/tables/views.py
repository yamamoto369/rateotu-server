from django.db.models import Prefetch
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from rateotu.accounts.permissions import IsCustomer, IsEmployee
from rateotu.tables.serializers import (
    TableSerializer,
    SeatReadSerializer,
    SeatWriteSerializer,
)
from rateotu.tables.models import Table, Seat
from rateotu.tables.services import update_seat_after_customer_selection


class TableListView(generics.ListAPIView):
    """
    List all tables in the restaurant.
    """

    permission_classes = [IsAuthenticated & (IsCustomer | IsEmployee)]
    serializer_class = TableSerializer

    def get_queryset(self):
        return Table.objects.prefetch_related(
            Prefetch("seats", queryset=Seat.objects.order_by("id"))
        ).order_by("table_number")


class SeatSwitchView(APIView):
    """
    Sit or unseat the authenticated user to a specific table seat.
    """

    multiple_lookup_fields = ["table_id", "pk"]
    permission_classes = [IsAuthenticated & (IsCustomer | IsEmployee)]
    read_serializer_class = SeatReadSerializer
    write_serializer_class = SeatWriteSerializer

    def get_queryset(self):
        return Seat.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        field_filter_lookups = {}
        for field in self.multiple_lookup_fields:
            field_filter_lookups[field] = self.kwargs[field]

        # To handle 404s (without DRF generics).
        obj = get_object_or_404(queryset, **field_filter_lookups)
        return obj

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        write_serializer = self.write_serializer_class(data=request.data)
        write_serializer.is_valid(raise_exception=True)

        validated_data = write_serializer.validated_data.copy()
        is_occupied = validated_data.get("is_occupied")
        updated_seat = update_seat_after_customer_selection(
            is_occupied, self.request.user.customer.id, instance.id
        )
        read_serializer = self.read_serializer_class(updated_seat)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(data=read_serializer.data, status=status.HTTP_200_OK)
