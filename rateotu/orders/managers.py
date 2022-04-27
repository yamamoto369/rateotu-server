from django.db.models.query import QuerySet


class OrderQuerySet(QuerySet):
    """
    Custom default QuerySet for the Order model.
    """

    def owned_by_user(self, user):
        return self.filter(customer=user)


OrderManager = OrderQuerySet.as_manager
