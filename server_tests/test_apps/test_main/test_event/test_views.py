import decimal
import json

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from server.apps.main.event.serializers import EventSerializerCreate
from server.json_tools import DecimalJSONEncoder


def test_api_root(client):
    """This test ensures that main API page works."""
    response = client.get('/api/')

    assert response.status_code == 200
    assert '/api/event/' in str(response.content)


class EventTests(TestCase):
    """Full Event CRUD + Admin test."""

    def setUp(self):
        """Set up test case."""
        super().setUp()
        serializer = EventSerializerCreate(data={
            'id': 'fake_id',
            'data': {
                'id': 'fake_id',
                'name': 'bar',
                'priceRanges': [{
                    'type': 'standard',
                    'currency': 'USD',
                    'min': decimal.Decimal('74.0'),
                    'max': decimal.Decimal('394.0'),
                }],
                'promoter': {
                    'name': 'DO NOT USE',
                },
                'dates': {
                    'start': {
                        'dateTime': '2020-08-08T19:00:00Z',
                    },
                },
            },
        })
        serializer.is_valid(raise_exception=True)
        self.sample_event = serializer.save()
        self.client = APIClient()

    def test_admin(self):
        """List and Get for django admin."""
        # login as fake admin
        user = User.objects.create(
            username='customer@example.com',
            email='customer@example.com',
            is_superuser=True,
            is_staff=True,
        )
        admin_client = APIClient()
        admin_client.force_login(user=user)

        response = admin_client.get('/admin/main/event/')
        assert response.status_code == 200
        assert 'fake_id' in str(response.content)

        response = admin_client.get(
            '/admin/main/event/{id}/change/'.format(id=self.sample_event.id),
        )
        assert response.status_code == 200
        assert 'fake_id' in str(response.content)

    def test_get_list(self):
        """Get list of all Events, should return one sample_event."""
        response = self.client.get('/api/event/')

        assert response.status_code == 200
        assert '"id":"fake_id"' in str(response.content)

    def test_get(self):
        """Get one sample_event."""
        response = self.client.get(
            '/api/event/{id}/'.format(id=self.sample_event.id),
        )
        assert response.status_code == 200
        assert '"id":"fake_id"' in str(response.content)

    def test_put(self):
        """Put (overwrite) sample_event."""
        response = self.client.put(
            path='/api/event/{id}/'.format(id=self.sample_event.id),
            data=json.dumps(
                {
                    'id': self.sample_event.id,
                    'cost_max': self.sample_event.cost_max,
                    'name': self.sample_event.name,
                    'cost_min': self.sample_event.cost_min,
                    'promoter_name': self.sample_event.promoter_name,
                    'start_date': self.sample_event.start_date,
                },
                cls=DecimalJSONEncoder,
            ),
            content_type='application/json',
        )
        assert response.status_code == 200, str(response.content)
        assert '"id":"fake_id"' in str(response.content)

    def test_post_delete(self):
        """Post (insert) new event and Delete it."""
        response = self.client.post(
            path='/api/event/',
            data=json.dumps(
                {
                    'id': 'sample2',
                    'data': {**self.sample_event.data, 'name': 'new_name'},
                },
                cls=DecimalJSONEncoder,
            ),
            content_type='application/json',
        )
        assert response.status_code == 201
        assert '"name":"new_name"' in str(response.content)

        response = self.client.delete('/api/event/sample2/')
        assert response.status_code == 204
