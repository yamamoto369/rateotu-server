from django.conf import settings
from django.contrib import admin
from django.urls import path, include


from rateotu.menus import urls as menu_urls
from rateotu.orders import urls as order_urls


urlpatterns = [
    path("admin/", admin.site.urls),
]

# Note: It's more REST API 'friendly' to have URLS without the ending forward slash
api_urlpatterns = [
    # Accounts (authentication, authorization, users)
    path("api/accounts/", include("rateotu.accounts.urls")),
    # Menus
    path("api/menus", include(menu_urls)),
    # Orders
    path("api/orders", include(order_urls)),
]

urlpatterns += api_urlpatterns

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ]
