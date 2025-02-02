from django.db import models
from django.conf import settings

from rateotu.tables.models import Table

# TODO: add https://github.com/makinacorpus/django-safedelete


class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customer"
    )
    table = models.ForeignKey(
        Table,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="customers",  # todo: assign
    )
    recieve_notification = models.BooleanField(
        default=True,
        verbose_name="Recieve Notifications",
        help_text="Recieve a notification when an order is ready",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.user.username
