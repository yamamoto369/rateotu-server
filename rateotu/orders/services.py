from django.db import transaction
from rateotu.orders.models import Order, OrderItem

# TODO: add mypy and Django/DRF stubs

# NOTE: Here we add our business logic (a class, func, etc)

# For instance, calling a web services (Celery tasks, etc)
# interacting with a database and other parts of our system


def create_customer_order(user, validated_data):
    with transaction.atomic():
        total = validated_data.pop("total")
        order_items = validated_data.pop("order_items")
        # NOTE: Set a customer instance based on a request user that
        # will be provided after authenticating trough JWT
        # We cannot trust a client to provide this piece of data!
        order = Order.objects.create(total=total, customer=user.customer)
        # NOTE: Bulk saving (1 INSERT query), due to performance and speed
        OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=order,
                    customer=user.customer,
                    item_id=item["id"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
                for item in order_items
            ]
        )
