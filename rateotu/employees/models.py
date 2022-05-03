from django.db import models
from django.conf import settings


class Employee(models.Model):
    ROLE_CHOICES = [
        ("waiter", "Waiter"),
        ("barman", "Barman"),
        ("chef", "Chef"),
    ]
    JOB_STATUS_CHOICES = [
        ("available", "Available"),
        ("busy", "Busy"),
        ("off duty", "Off-duty"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="employee"
    )
    role = models.CharField(
        max_length=25,
        choices=ROLE_CHOICES,
        verbose_name="Job role (title)",
        help_text="Job function within restaurant",
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name="Biography",
        help_text="Short biography about employee",
    )
    salary = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name="Monthly Salary",
        help_text="Monthly salary in space £",
    )
    location = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Location (Address)",
        help_text="Location of residence on the planet Dentrass",
    )
    # TODO: If need (but makes no sense, time is not linear troughout universe)
    dob = models.DateField(
        blank=True,
        null=True,
        verbose_name="Date of birth",
        help_text="Date of birth based on something (??)",
    )
    job_status = models.CharField(
        max_length=25,
        choices=JOB_STATUS_CHOICES,
    )

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    def __str__(self):
        return f"Employee: {self.user} - Role: {self.role}"

    @property
    def is_chef(self):
        return self.role == "chef"

    @property
    def is_barman(self):
        return self.role == "barman"

    @property
    def is_waiter(self):
        return self.role == "waiter"

    @property
    def is_available(self):
        """
        To distinguish between available and busy (duty or off-duty)
        """
        return True if self.job_status == "available" else False
