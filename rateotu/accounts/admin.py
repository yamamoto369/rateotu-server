from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from rateotu.accounts.forms import UserChangeForm, UserCreationForm
from rateotu.employees.admin import EmployeeInline

User = get_user_model()


class UserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    inlines = (EmployeeInline,)
    list_display = ["username", "email", "is_active", "is_employee", "is_customer"]
    search_fields = ["username", "email", "is_employee", "is_customer"]
    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {
                "fields": (
                    "galaxy",
                    "star_system",
                    "home_planet",
                    "planet",
                    "colony",
                    "species",
                ),
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": (
                    "galaxy",
                    "star_system",
                    "home_planet",
                    "planet",
                    "colony",
                    "species",
                ),
            },
        ),
    )


admin.site.register(User, UserAdmin)
