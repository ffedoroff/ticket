import logging

import jsonschema
from rest_framework import serializers

from server.apps.main.event.event_schema import EVENT_SCHEMA
from server.apps.main.event.models import Event

logger = logging.getLogger(__name__)


class EventSerializerCreate(serializers.ModelSerializer):
    """Simple Event serializer."""

    class Meta(object):
        model = Event
        fields = [
            'id',
            'cost_max',
            'cost_min',
            'created',
            'data',
            'modified',
            'name',
            'promoter_name',
            'start_date',
        ]
        read_only_fields = [
            'cost_max',
            'cost_min',
            'created',
            'modified',
            'name',
            'promoter_name',
            'start_date',
        ]
        extra_kwargs = {
            'data': {'write_only': True, 'required': True},
        }

    def validate_data(self, value):  # noqa: WPS110
        """Check proper "data" field structure."""
        try:
            jsonschema.validate(instance=value, schema=EVENT_SCHEMA)
        except jsonschema.exceptions.ValidationError as error:
            raise serializers.ValidationError(detail=error.args[0])
        return value

    def validate(self, data):  # noqa: WPS110
        """Validates data, update other fields based on data."""
        super().validate(data)
        if 'data' not in data:
            return data
        raw_data = data['data']
        data['cost_max'] = raw_data['priceRanges'][0]['max']
        data['cost_min'] = raw_data['priceRanges'][0]['min']
        data['name'] = raw_data['name']
        data['promoter_name'] = raw_data['promoter']['name']
        data['start_date'] = raw_data['dates']['start']['dateTime']
        return data


class EventSerializer(EventSerializerCreate):
    """EventSerializer for REST API (without data)."""

    class Meta(EventSerializerCreate.Meta):
        fields = [
            'id',
            'cost_max',
            'cost_min',
            'created',
            'modified',
            'name',
            'promoter_name',
            'start_date',
        ]
        read_only_fields = ['created', 'modified']
        extra_kwargs = {}  # type: ignore
