from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    # dasboard url
    path("", views.dashboard, name="dashboard"),
    # Inventory appllication URLs
    path("inventory/", include("inventory.urls")),
    # Subdealers appllication URLs
    path("subdealers/", include("SubDealers.urls")),
    # Employee Application URLs
    path("employees/",include("employees.urls")),
]
