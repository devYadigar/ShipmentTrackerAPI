"""Url mappings for the shipment app"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from shipment import views

router = DefaultRouter()
router.register('shipment', views.ShipmentViewSet)

app_name = 'shipment'

urlpatterns = [
    path('', include(router.urls)),
]
