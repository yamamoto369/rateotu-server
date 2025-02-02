from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator

from rateotu.orders.managers import OrderManager
from rateotu.customers.models import Customer
from rateotu.menus.models import Item
from rateotu.tables.models import Table

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

    # Max 9,999,999,999.99 (10B of 'space £')
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        verbose_name="Total Amount",
        help_text="Total amount in space £",
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    table = models.ForeignKey(
        Table,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="orders",  # todo: assign
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
    served_at = models.DateTimeField(blank=True, null=True)  # TODO: table

    objects = OrderManager()

    def __str__(self):
        return f"{self.id} - {self.order_status}"


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
    table = models.ForeignKey(
        Table,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="order_items",  # todo: assign
    )
    # Max 999,999.99 (1M of 'space £')
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
    # Consider adding 'category_name' to reduce amount of joins
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

    # TODO_ N+1, override base get_queryset
    def __str__(self):
        return f"{self.id} - {self.item.name}"
