from django.db.models.query import QuerySet

# TODO: Add more manager methods to keep it DRY


class OrderQuerySet(QuerySet):
    """
    Custom default QuerySet for the Order model.
    """

    def owned_by_user(self, user):
        return self.filter(customer=user)


OrderManager = OrderQuerySet.as_manager
