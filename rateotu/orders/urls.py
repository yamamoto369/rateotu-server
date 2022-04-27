from django.urls import path

from rateotu.orders import views


app_name = "orders"
urlpatterns = [
    path("", views.OrderListCreateView.as_view(), name="order-list-create"),
]
