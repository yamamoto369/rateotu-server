from django.urls import path

from rateotu.orders import views


app_name = "orders"
urlpatterns = [
    path("", views.OrderListCreateView.as_view(), name="order-list-create"),
    path("/items", views.OrderItemListView.as_view(), name="order-item-list"),
    path(
        "/items/<int:pk>", views.OrderItemDetailView.as_view(), name="order-item-detail"
    ),
    path(
        "/items/bulk-update",
        views.OrderItemBulkUpdateView.as_view(),
        name="order-item-bulk-update",
    ),
]
