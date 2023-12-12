"""Test for Shipment API"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Shipment

from shipment.serializers import ShipmentSerializer


SHIPMENT_URL = reverse('shipment:shipment-list')


def create_shipment(user, **params):
    """Create and return a simple shipment"""
    defaults = {
        'origin': 'Baku',
        'destination': 'Tallinn',
        'status': 'pending'
    }
    defaults.update(params)

    return Shipment.objects.create(user=user, **defaults)


class PublicShipmentAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(SHIPMENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateShipmentAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'test123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_shipments(self):
        create_shipment(user=self.user)
        create_shipment(user=self.user)

        res = self.client.get(SHIPMENT_URL)

        shipments = Shipment.objects.all().order_by('-id')
        serializer = ShipmentSerializer(shipments, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_shipment_list_limited_to_user(self):
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'test123'
        )
        create_shipment(user=other_user)
        create_shipment(user=self.user)

        res = self.client.get(SHIPMENT_URL)

        shipments = Shipment.objects.filter(user=self.user)
        serializer = ShipmentSerializer(shipments, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_shipment(self):
        payloads = [
            {
                'origin': 'Baku',
                'destination': 'Tallinn',
                'status': 'pending'
            },
            {
                'origin': 'Baku',
                'destination': 'Tallinn'
            }
        ]
        for payload in payloads:
            res = self.client.post(SHIPMENT_URL, payload)
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
            shipment = Shipment.objects.get(id=res.data['id'])
            for k, v in payload.items():
                self.assertEqual(getattr(shipment, k), v)
            self.assertEqual(shipment.user, self.user)

    def test_update_shipment(self):
        shipment = create_shipment(user=self.user)

        right_payload = {
            'origin': 'Baku',
            'destination': 'Tallinn'
        }

        res = self.client.patch(f"{SHIPMENT_URL}{shipment.id}/", right_payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        wrong_payload = {
            'origin': 'Baku',
            'destination': 'Tallinn',
            'status': 'pending'
        }

        res = self.client.patch(f"{SHIPMENT_URL}{shipment.id}/", wrong_payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_shipment(self):
        shipment = create_shipment(user=self.user)

        res = self.client.delete(f"{SHIPMENT_URL}{shipment.id}/")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Shipment.objects.filter(id=shipment.id).exists())



