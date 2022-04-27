from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsEmployee(BasePermission):
    """
    Custom IsEmployee permission.

    Allows HTTP access only to employee users.
    """

    # NOTE: View-level (API level) permission
    def has_permission(self, request, view):
        return request.user and request.user.is_employee

    # NOTE: Instance-level (API level) permission
    # Requires an extra query, not needed for now
    def has_object_permission(self, request, view, obj):
        return True


class IsCustomer(BasePermission):
    """
    Custom IsEmployee permission.

    Allows HTTP access only to customer users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_customer

    def has_object_permission(self, request, view, obj):
        return True


class ReadOnly(BasePermission):
    """
    Allows HTTP access to users only if the request method is read-only
    (GET, HEAD, OPTIONS) — all read-only and safe.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
