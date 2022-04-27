from django.contrib import admin

from rateotu.employees.models import Employee


class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False


class EmployeeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Employee, EmployeeAdmin)
