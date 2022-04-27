from django.contrib import admin

from rateotu.customers.models import Customer


class CustomerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Customer, CustomerAdmin)
