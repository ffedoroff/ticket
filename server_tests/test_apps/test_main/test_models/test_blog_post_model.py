
from hypothesis import given, strategies
from hypothesis.extra import django

from server.apps.main.event.models import Event


class TestEvent(django.TestCase):
    """This is a property-based test that ensures model correctness."""

    @given(django.from_model(Event, data=strategies.just({'foo': 'bar'})))
    def test_model_properties(self, instance):
        """Tests that instance can be saved and has correct representation."""
        instance.save()
        assert instance.id
