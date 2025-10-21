from . import views
from django.urls import path

urlpatterns = [
    path("add-products/", views.add_product, name="Add_product"),
    path("manage-products/", views.manage_products, name="manage_products"),
]
