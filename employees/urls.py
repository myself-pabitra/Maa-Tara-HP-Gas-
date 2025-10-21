from . import views
from django.urls import path

urlpatterns = [
    path("add-new-employee/", views.add_new_employees, name="add_new_employees"),
    ]