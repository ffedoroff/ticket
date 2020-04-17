import pytest
from django.core.management import call_command

from server.apps.main.event.models import Event


@pytest.mark.vcr(record_mode='once', match_on=['body', 'method', 'uri'])
@pytest.mark.django_db
def test_get_events():
    """Call get_tickets django command few times."""
    assert Event.objects.all().count() == 0

    # first page should insert 20 Events into db
    call_command('get_events', max_pages=1)
    assert Event.objects.all().count() == 20

    # delete one Event, make sure it inserts again
    Event.objects.all().first().delete()
    assert Event.objects.all().count() == 19

    # first page should keep the same 20 Events into db
    call_command('get_events', max_pages=1)
    assert Event.objects.all().count() == 20

    # 3 pages should insert/update 58 Events into db (2 events duplicated)
    call_command('get_events', max_pages=3)
    assert Event.objects.all().count() == 55
