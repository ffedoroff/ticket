import logging

from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet

from server.apps.main.event.models import Event

logger = logging.getLogger(__name__)


class EventSerializer(serializers.ModelSerializer):
    """Simple Event serializer."""

    class Meta(object):
        model = Event
        fields = (
            'created',
            'data',
            'id',
            'modified',
        )
        read_only_fields = (
            'created',
            'modified',
        )

    def validate_data(self, value):
        """Check proper "data" field structure."""
        errors = []

        # make sure "start date" structure correct
        if not value.get('dates', {}).get('start', {}).get('dateTime', None):
            errors.append('start_date incorrect')

        # make sure "cost_min" and "cost_max" structure correct
        price_ranges = value.get('priceRanges', [])
        if not isinstance(price_ranges, list) or len(price_ranges) != 1:
            errors.append('price_ranges incorrect')
        else:
            price_ranges = price_ranges[0]
            if (
                not isinstance(price_ranges, dict) or
                price_ranges.get('type', '') != 'standard' or
                price_ranges.get('currency', '') != 'USD' or
                not price_ranges.get('min', '') or
                not price_ranges.get('max', '')
            ):
                errors.append('price_ranges incorrect')

        if errors:
            raise serializers.ValidationError(detail=errors)
        return value

    def validate(self, data):
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


class EventViewSet(ModelViewSet):
    """Simple Event ViewSet CRUD."""

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_fields = (
        'status_code',
        'user_id',
    )
    # event name, event start date, promoter name, ticket cost (min and max for a standard price).
    ordering = ('created',)
