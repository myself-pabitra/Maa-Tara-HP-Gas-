from . import views
from django.urls import path

urlpatterns = [
    path("add-subdealers/", views.CreateNewSubDealers, name="CreateNewSubDealers"),
    path('add-subdealers-product-discount/',views.addSubDealersProductDiscount,name='addSubDealersProductDiscount'),
    path("view-discounts/", views.view_subdealer_discounts, name="view_subdealer_discounts"),
]
