from rateotu.customers.models import Customer

# TODO: add mypy and Django/DRF stubs


def create_customer(user):
    return Customer.objects.create(user=user)
