from django.db import transaction

from rateotu.customers.models import Customer
from rateotu.tables.models import Seat

# TODO: Add mypy and Django/DRF stubs.


@transaction.atomic
def update_seat_after_customer_selection(is_occupied_choice, customer_id, seat_id):
    """
    Assign or unassign the given table seat for the given customer user.
    """
    # Row-level locks to prevent updates with race conditions.
    # This function can be used anywhere in the system (request-response cycle,
    # Celery tasks, external scripts, etc).
    # Therefore when a database operation is in progress, the object or the qs
    # of objects that are being updated must be locked until the operation is complete,
    # so that no other process (or thread) can access this qs objects.
    seat = Seat.objects.select_for_update().get(id=seat_id)
    customer = Customer.objects.select_for_update().get(id=customer_id)

    if is_occupied_choice:
        seat.is_occupied = True
        seat.customer = customer
        customer.table = seat.table
    else:
        seat.is_occupied = False
        seat.customer = None
        customer.table = None

    seat.save()
    customer.save()

    return seat
