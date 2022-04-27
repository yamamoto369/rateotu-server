from rateotu.customers.models import Customer

# TOOD: add mypy and Django/DRF stubs


def create_customer(user):
    return Customer.objects.create(user=user)
