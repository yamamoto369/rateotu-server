from django.db import models
from django.core.exceptions import ValidationError


class Table(models.Model):
    TABLE_NUMBER_CHOICES = [
        ("a1", "a1"),
        ("a2", "a2"),
        ("a3", "a3"),
    ]

    # Physical table location (MAX: 234 tables)
    table_number = models.CharField(max_length=2, choices=TABLE_NUMBER_CHOICES)
    seat_capacity = models.IntegerField(default=8, verbose_name="Max Seat Capacity")
    is_available = models.BooleanField(
        default=True, help_text="Is the table available to customers"
    )
    is_full = models.BooleanField(default=False)  # set automatically
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def available_seat_capacity(self):
        return (
            self.seat_capacity
            - Seat.objects.filter(table=self, is_occupied=True).count()
        )

    # def save(self, *args, **kwargs):
    #    self.is_available = self.capacity - self.get_queryset().filter()
    #    super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.table_number}"


class Seat(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="seats")
    customer = models.OneToOneField(
        "customers.Customer",  # Fixes circular import issue
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="seat",
    )
    is_occupied = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if (
            not self.pk
            and self.get_queryset().filter(table=self.table).count()
            >= self.table.seat_capacity
        ):
            raise ValidationError("Only 8 seats per table allowed!")

    def __str__(self):
        return f"{self.table} - {self.customer} - {self.is_occupied}"
