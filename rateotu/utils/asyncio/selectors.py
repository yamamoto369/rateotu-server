from django.contrib.auth import get_user_model

from channels.db import database_sync_to_async


User = get_user_model()


# This decorator turns ORM query from sync to async
# and cleans up database connections on exit.
@database_sync_to_async
def get_user(field_name, value):
    """
    Tries to fetch a User obj for a given field_name=value.
    """
    return User.objects.get(**{field_name: value})


@database_sync_to_async
def get_employee_for_user(user):
    """
    Tries to fetch Employee obj for a given user.
    """
    return user.employee
