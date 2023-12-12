from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Shipment
from shipment import serializers


class ShipmentViewSet(viewsets.ModelViewSet):
    """View for manage shipment api"""
    serializer_class = serializers.ShipmentSerializer
    queryset = Shipment.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve shipments for authenticated user.
        Check if user is superuser, then return all the shipments.
        """
        user = self.request.user
        if user.is_superuser:
            return self.queryset.order_by('-id')
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        """Create a new shipment"""
        serializer.save(user=self.request.user)
