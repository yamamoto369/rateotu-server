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


# Method decorated with @transaction.atomic to ensure
# logic is executed in a single transaction
@transaction.atomic
def create_customer_order(customer, total, order_items):
    """
    Creates the order for the given customer instance
    and creates all order items linked to the order.
    """
    # Sets a customer instance based on a request user (check views)
    # that will be provided after authenticating trough JWT auth.
    # We cannot trust a client to provide this piece of data!
    order = Order.objects.create(total=total, customer=customer)
    # Bulk INSERT (1 query), due to performance and speed.
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


@transaction.atomic
def bulk_update_order_items_order_status(order_item_ids, order_status):
    """
    Bulk update 'order_status' on all OrderItem instances for a given
    'order_item_ids' iterable.
    """
    # Row-level locks to prevent updates with race conditions.
    # This function can be used anywhere in the system (request-response cycle,
    # Celery tasks, external scripts, etc).
    # Therefore when a database operation is in progress, the object or the qs
    # of objects that are being updated must be locked until the operation is complete,
    # so that no other process (or thread) can access this qs objects.
    order_items = OrderItem.objects.select_for_update().filter(id__in=order_item_ids)
    # Loop over each item and invoke save() on instance.
    for order_item in order_items:
        order_item.order_status = order_status
        # save() method called on each intance to update (signals are triggerd as well).
        order_item.save()
