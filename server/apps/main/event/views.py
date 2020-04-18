import logging

import rest_framework_filters as filters
from rest_framework.viewsets import ModelViewSet

from server.apps.main.event.models import Event
from server.apps.main.event.serializers import (
    EventSerializer,
    EventSerializerCreate,
)

logger = logging.getLogger(__name__)


class EventFilter(filters.FilterSet):
    """Full filter functional for all fields except data."""

    cost_max = filters.AutoFilter(lookups='__all__')
    cost_min = filters.AutoFilter(lookups='__all__')
    created = filters.AutoFilter(lookups='__all__')
    modified = filters.AutoFilter(lookups='__all__')
    name = filters.AutoFilter(lookups='__all__')
    promoter_name = filters.AutoFilter(lookups='__all__')
    start_date = filters.AutoFilter(lookups='__all__')
    search_fields = ['name', 'promoter_name']

    class Meta(object):
        model = Event
        exclude = 'data'


class EventViewSet(ModelViewSet):
    """Simple Event ViewSet CRUD."""

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_class = EventFilter

    def get_serializer(self, *args, **kwargs):
        """Change serializer when CREATE calls."""
        if self.action == 'create':
            return EventSerializerCreate(*args, **kwargs)
        return self.serializer_class(*args, **kwargs)
