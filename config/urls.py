from django.conf import settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
]

api_urlpatterns = [
    # Accounts (authentication, authorization, users)
    path("api/accounts/", include("rateotu.accounts.urls")),
]

urlpatterns += api_urlpatterns

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ]
