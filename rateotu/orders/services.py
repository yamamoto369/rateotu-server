"""
# Here we add our orders-related business logic (a class, func, etc).
# For instance, calling an internal or external services (e.g. if blocking,
# then we should use Celery task queue without blocking our main Django thread),
# interacting with a database (DML/pushing or deleting data to/from the database)
# and other parts of our system, etc.
# This can also be a module inside the services package (in an advanced stage
# of the project)

# TODO: Add mypy and Django/DRF stubs.
"""
import logging

from django.db import transaction

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from rateotu.employees.selectors import get_available_employees
from rateotu.orders.serializers import OrderItemSerializer
from rateotu.orders.models import Order, OrderItem

logger = logging.getLogger("rateotu")


# Method decorated with @transaction.atomic to ensure
# logic is executed in a single transaction
@transaction.atomic
def create_customer_order(customer, total, order_items):
    """
    Creates the order for the given customer instance
    and all order items linked to the order.
    """
    # Sets a customer instance based on a request user (SEE: views)
    # that will be provided after authenticating trough JWT auth.
    # We cannot trust a client to provide this piece of data!
    order = Order.objects.create(total=total, customer=customer)
    # Bulk INSERT (1 query), due to performance and speed.
    created_order_items = OrderItem.objects.bulk_create(
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
    notify_chefs_and_barmans_about_created_order(created_order_items)
    return created_order_items


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
    ready_order_items = []
    # Loop over each item and invoke save() on instance.
    for order_item in order_items:
        order_item.order_status = order_status
        # save() method called on each intance to update (signals are triggerd as well).
        order_item.save()

        if order_item.order_status == "ready":
            ready_order_items.append(order_item)

    if ready_order_items:
        return notify_waiter_about_ready_order_items(ready_order_items)


def notify_chefs_and_barmans_about_created_order(created_order_items):
    chef_order_items = []
    barman_order_items = []

    # TODO: Profile (prob N+1).
    # Make 'create_customer_order()' return <QuerySet [<OrderItem,..]
    # instead of [<OrderItem,...]
    for order_item in created_order_items:
        if order_item.item.category.name == "food":
            chef_order_items.append(order_item)
        elif order_item.item.category.name == "drink":
            barman_order_items.append(order_item)

    if chef_order_items:
        notify_chefs_about_created_order(chef_order_items)
    if barman_order_items:
        notify_barmans_about_created_order(barman_order_items)


def notify_chefs_about_created_order(created_order_items):
    available_chefs = get_available_employees(role="chef")

    if not available_chefs.exists():
        # If needed we can mail/notify admins/managers when this happens
        # (SEE: logging in settings/base)
        logger.info(
            f"""There are no chefs available to prepare food order items:
            {[obj.id for obj in created_order_items]}""",
        )
        return False

    # fmt: off
    send_order_notification_to_available_employees(
        created_order_items,
        available_chefs
    )
    # fmt: on
    return True


# The barman can choose to serve order items in a batches, or
# based on his assessment of the situation (or the restaurant rules).
# He does this by clicking in his dashboard on a selected items for a given order.
def notify_barmans_about_created_order(created_order_items):
    available_barmans = get_available_employees(role="barman")

    if not available_barmans.exists():
        # If needed we can mail/notify admins/managers when this happens
        # (SEE: logging in settings/base)
        logger.info(
            f"""There are no barmans available to prepare drink order items:
            {[obj.id for obj in created_order_items]}""",
        )
        return False

    send_order_notification_to_available_employees(
        created_order_items, available_barmans
    )
    return True


def notify_waiter_about_ready_order_items(ready_order_items):
    available_waiters = get_available_employees(role="waiter")
    random_available_waiter = available_waiters.order_by("?").first()

    if not random_available_waiter:
        # If needed we can mail/notify admins/managers when this happens
        # (SEE: logging in settings/base)
        logger.info(
            f"""There is no waiter available to serve ready order items:
            {[obj.id for obj in ready_order_items]}""",
        )
        return False

    send_order_notification_to_available_employees(
        ready_order_items, [random_available_waiter]
    )
    return True


def send_order_notification_to_available_employees(order_items, employees):
    channel_layer = get_channel_layer()
    for order_item in order_items:
        for employee in employees:
            async_to_sync(channel_layer.group_send)(
                f"ws_employee_{employee.id}_{employee.role}",
                {
                    "type": "broadcast_to_employees",
                    "payload": OrderItemSerializer(order_item).data,
                },
            )
    return True
