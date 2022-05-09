from django.urls import path

from rateotu.tables import views


app_name = "tables"
urlpatterns = [
    path("", views.TableListView.as_view(), name="table-list"),
    path(
        "/<int:table_id>/seats/<int:pk>/switch-seat",
        views.SeatSwitchView.as_view(),
        name="seat-switch",
    ),
]
