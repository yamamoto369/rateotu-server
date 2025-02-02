from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from rateotu.accounts.urls import employee_urlspatterns, customer_urlpatterns
from rateotu.menus import urls as menu_urls
from rateotu.orders import urls as order_urls
from rateotu.tables import urls as restaurant_table_urls
from rateotu.employees import urls as employee_urls


urlpatterns = [
    path("admin/", admin.site.urls),
]

# It's more REST API 'friendly' to have URLS without the ending forward slash
api_urlpatterns = [
    # Accounts (authentication, authorization, users)
    path("api/accounts/", include(customer_urlpatterns)),  # — employees and customers
    path("api/emp/accounts/", include(employee_urlspatterns)),  # — employees only
    # Menus
    path("api/menus", include(menu_urls)),
    # Orders
    path("api/orders", include(order_urls)),
    # Tables
    path("api/tables", include(restaurant_table_urls)),
    # Employees
    path("api/employees", include(employee_urls)),
]

urlpatterns += api_urlpatterns

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += [
        path("drf-auth/", include("rest_framework.urls")),
        path("__debug__/", include("debug_toolbar.urls")),
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ]
