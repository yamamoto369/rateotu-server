from django.contrib import admin
from rateotu.tables.models import Table, Seat


class SeatInline(admin.TabularInline):
    model = Seat
    can_delete = False


class TableAdmin(admin.ModelAdmin):
    list_display = [
        "table_number",
        "seat_capacity",
        "available_seat_capacity",
        "is_full",
        "updated_at",
    ]
    list_filter = [
        "is_full",
    ]


class SeatAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "table",
        "customer",
        "is_occupied",
        "updated_at",
    ]
    list_filter = [
        "is_occupied",
    ]


admin.site.register(Table, TableAdmin)
admin.site.register(Seat, SeatAdmin)
