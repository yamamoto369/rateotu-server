from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator

from rateotu.customers.models import Customer
from rateotu.menus.models import Item
from rateotu.orders.managers import OrderManager

# TODO: add https://github.com/makinacorpus/django-safedelete


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ("created", "Created"),
        ("preparing", "Preparing"),
        ("ready", "Ready"),
        ("served", "Served"),
        ("serving", "Serving"),
        ("cancelled", "Cancelled"),
    ]
    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("not paid", "Not paid"),
    ]

    # NOTE: Max 9,999,999,999.99 (10B of 'space £')
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        verbose_name="Total Amount",
        help_text="Total amount in space £",
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_status = models.CharField(
        max_length=25,
        choices=ORDER_STATUS_CHOICES,
        default=ORDER_STATUS_CHOICES[0][0],
    )
    payment_status = models.CharField(
        max_length=25,
        choices=PAYMENT_STATUS_CHOICES,
        default=PAYMENT_STATUS_CHOICES[2][0],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    served_at = models.DateTimeField(blank=True, null=True)  # TODO: table

    objects = OrderManager()

    def __str__(self):
        return self.order_status


# NOTE: Manual M:N relationship (allows us to add a custom fields)
class OrderItem(models.Model):
    ORDER_STATUS_CHOICES = [
        ("created", "Created"),
        ("preparing", "Preparing"),
        ("ready", "Ready"),
        ("served", "Served"),
        ("serving", "Serving"),
        ("cancelled", "Cancelled"),
    ]
    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("not paid", "Not paid"),
    ]

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="order_items"
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="order_items")
    # NOTE: Max 999,999.99 (1M of 'space £')
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        help_text="Price in space £",
    )
    quantity = models.PositiveIntegerField(
        help_text="""If a customer orders a multiple of the same food or drink,
                     or for a pre made food and drinks which can be served in
                     restaurants (e.g. cans of something, sweets, etc)""",
    )
    order_status = models.CharField(
        max_length=25,
        choices=ORDER_STATUS_CHOICES,
        default=ORDER_STATUS_CHOICES[0][0],
    )
    payment_status = models.CharField(
        max_length=25,
        choices=PAYMENT_STATUS_CHOICES,
        default=PAYMENT_STATUS_CHOICES[2][0],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    served_at = models.DateTimeField(blank=True, null=True)

    # TODO_ N+1
    def __str__(self):
        return self.item.name
