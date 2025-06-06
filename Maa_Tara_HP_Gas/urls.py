from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    # dasboard url
    path("", views.dashboard, name="dashboard"),
    # Inventory appllication URLs
    path("inventory/", include("inventory.urls")),
]
