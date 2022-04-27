from django.dispatch import receiver

from djoser.signals import user_activated

from rateotu.customers.services import create_customer


@receiver(user_activated)
def user_activated_handler(sender, user, request, *args, **kwargs):
    """
    Creates a Customer instance, after the user successfully activates
    his account (e-mail activation) over the REST API endpoint.

    Note: We do it this way (using Djoser signals) as it allows use to
    separate the User creation by an anoymous user (a potential customer)
    instead of internally created User (can be triggered by admins/stuff,
    or in the other places in code - 'post_save').
    """
    create_customer(user)
