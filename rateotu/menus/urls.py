from django.urls import path

from rateotu.menus import views


app_name = "menus"
urlpatterns = [
    path("", views.MenuListView.as_view(), name="menu-list"),
]
