from django.db import models
from django.contrib.auth.models import AbstractUser

# CAVEAT: Authentication is not performed lazily in DRF
# SEE: https://github.com/encode/django-rest-framework/issues/6002


class User(AbstractUser):
    # TODO: Automatically assign after user UI registration
    # TODO: Add some fantasy-related validations
    galaxy = models.CharField(max_length=255, blank=True)
    star_system = models.CharField(max_length=255, blank=True)
    planet = models.CharField(max_length=255, blank=True, verbose_name="Current planet")
    home_planet = models.CharField(max_length=255, blank=True)
    colony = models.CharField(max_length=255, blank=True)
    species = models.CharField(
        max_length=255, blank=True, help_text="Creature race/species"
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_employee(self):
        if self.is_superuser:
            return True
        return self.is_staff

    @property
    def is_customer(self):
        return not self.is_employee

    @property
    def permission_role(self):
        return "employee" if self.is_employee else "customer"
