from rateotu.employees.models import Employee


def get_available_employees(role):
    return Employee.objects.filter(role=role, job_status="available")
