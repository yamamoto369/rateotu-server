from django.urls import path

from rateotu.employees import views


app_name = "employees"
urlpatterns = [
    path(
        "/dashboard-data",
        views.EmployeeDashboardDataView.as_view(),
        name="dashboard-data",
    ),
]
