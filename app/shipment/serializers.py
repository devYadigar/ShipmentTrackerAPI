from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from core.models import Shipment


class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = [
            'id', 'origin', 'destination', 'status', 'date_shipped'
        ]
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        user = self.context['request'].user

        validated_data.pop('user', None)

        if user.is_superuser:
            # Superuser can only update 'status' field
            if any(field != 'status' for field in validated_data):
                raise ValidationError({
                    'error': 'Superuser only allowed to update the status.'
                })
            instance.status = validated_data.get('status', instance.status)
        else:
            # Other users can update all fields except 'status'
            if 'status' in validated_data:
                raise ValidationError({
                    'status': 'You do not have permission to update status.'
                })
            for field, value in validated_data.items():
                setattr(instance, field, value)

        instance.save()
        return instance
