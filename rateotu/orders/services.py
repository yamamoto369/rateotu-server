"""
# NOTE: Here we add our orders-related business logic (a class, func, etc).
# For instance, calling an internal or external services (e.g. if blocking,
# then we should use Celery task queue without blocking our main Django thread),
# interacting with a database (DML/pushing or deleting data to/from the database)
# and other parts of our system, etc.
# NOTE: This can also be a module inside the services package (in an advanced stage
# of the project)

# TODO: Add mypy and Django/DRF stubs.
"""

from django.db import transaction
from rateotu.orders.models import Order, OrderItem


@transaction.atomic
def create_customer_order(customer, total, order_items):
    """
    Creates the order for the given customer instance
    and creates all order items linked to the order.
    """
    # NOTE: Sets a customer instance based on a request user (check views)
    # that will be provided after authenticating trough JWT auth.
    # We cannot trust a client to provide this piece of data!
    order = Order.objects.create(total=total, customer=customer)
    # NOTE: Bulk saving (1 INSERT query), due to performance and speed.
    OrderItem.objects.bulk_create(
        [
            OrderItem(
                order=order,
                customer=customer,
                item_id=item["id"],
                price=item["price"],
                quantity=item["quantity"],
            )
            for item in order_items
        ]
    )
