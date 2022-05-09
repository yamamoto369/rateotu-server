from django.contrib import admin

from rateotu.orders.models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "total",
        "order_status",
        "payment_status",
        "created_at",
        "updated_at",
    ]


class OrderItemAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("item")


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
