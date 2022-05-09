from django.db.models import F, Sum, Case, When, Value as V, IntegerField, DecimalField
from django.db.models.functions import Coalesce, TruncDate

from rateotu.employees.models import Employee
from rateotu.orders.models import Order, OrderItem


def get_available_employees(role):
    return Employee.objects.filter(role=role, job_status="available")


def get_order_item_quantity_totals_per_category():
    return OrderItem.objects.aggregate(
        food=Coalesce(
            Sum(
                Case(
                    When(item__category__name="food", then=F("quantity")),
                    default=0,
                    output_field=IntegerField(),
                )
            ),
            V(0),
        ),
        drink=Coalesce(
            Sum(
                Case(
                    When(item__category__name="drink", then=F("quantity")),
                    default=0,
                    output_field=IntegerField(),
                )
            ),
            V(0),
        ),
    )


def get_order_item_quantity_totals_per_day():
    return (
        OrderItem.objects.annotate(date=TruncDate("created_at"))
        .values("date")
        .annotate(order_items=Sum("quantity"))
        .order_by("date")
    )


def get_total_orders_count():
    return Order.objects.count()


def get_total_orders_revenue():
    return OrderItem.objects.aggregate(
        revenue=Coalesce(
            Sum(F("quantity") * F("price")), V(0), output_field=DecimalField()
        )
    )["revenue"]


def get_total_orders_quantity():
    return OrderItem.objects.aggregate(
        quantity=Coalesce(Sum(F("quantity")), V(0), output_field=IntegerField())
    )["quantity"]


def get_total_distinct_customers():
    return Order.objects.distinct("customer").count()


def get_best_sellers():
    pass
