from django.test import TestCase
from django.contrib.auth import get_user_model

from .. import models


class ShipmentTest(TestCase):
    def test_create_shipment(self):
        user = get_user_model().objects.create_user(
            'test@example.com',
            'test123'
        )
        data = {
            'user': user,
            'origin': 'Baku',
            'destination': 'Tallinn',
            'status': 'pending'
        }
        shipment = models.Shipment.objects.create(**data)

        self.assertEqual(
            str(shipment),
            "Shipment from " +
            f"{data['origin']} to {data['destination']} " +
            f"({data['status']})")
