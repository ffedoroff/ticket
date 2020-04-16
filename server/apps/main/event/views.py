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


class EventViewSet(ModelViewSet):
    """Simple Event ViewSet CRUD."""

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_fields = (
        'status_code',
        'user_id',
    )
    ordering = ('created',)
