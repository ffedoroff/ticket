import json
import logging
from urllib import request

from django.conf import settings
from django.core.management.base import BaseCommand
from tqdm import tqdm

from server.apps.main.event.models import Event
from server.apps.main.event.serializers import EventSerializerCreate

logger = logging.getLogger(__name__)

_ID = 'id'
_MAX_PAGES = 100  # max pages to download
_DEFAULT_PAGES = 50  # pages to download by default


class Command(BaseCommand):
    """
    Download and save Events into db.

    python manage.py get_events --max-pages=3
    """

    def add_arguments(self, parser):
        """Basic args."""
        parser.add_argument(
            '--max-pages',
            type=int,
            default=_DEFAULT_PAGES,
            help='how many pages should be parsed 1-100 (default 50)',
            metavar='[1-{_MAX_PAGES}]'.format(_MAX_PAGES=_MAX_PAGES),
            choices=range(1, _MAX_PAGES + 1),
        )

    def handle(  # type: ignore # noqa: WPS110, WPS210
        self,
        max_pages: int,
        **options,
    ):
        """Django main handle."""
        logger.info(
            'get_events max_pages={max_pages} options={options}'.format(
                max_pages=max_pages,
                options=options,
            ),
        )

        # for the first page, generates full url manually
        url = '{api}/discovery/v2/events.json?apikey={key}'.format(
            api=settings.TICKETMASTER_API_ENDPOINT,
            key=settings.TICKETMASTER_API_KEY,
        )
        for _ in tqdm(range(max_pages)):  # noqa: WPS122
            response = json.loads(request.urlopen(url).read())  # noqa: S310

            for event_data in response['_embedded']['events']:
                event_id = event_data[_ID]
                serializer_data = {_ID: event_id, 'data': event_data}
                logger.info('saving event {id}'.format(id=event_id))

                self._save_event(event_id, serializer_data)

            next_page = response['_links']['next']['href']
            url = '{api}{next_page}&apikey={key}'.format(
                api=settings.TICKETMASTER_API_ENDPOINT,
                next_page=next_page,
                key=settings.TICKETMASTER_API_KEY,
            )
            logger.info('getting {next_page}'.format(next_page=next_page))

    def _save_event(self, event_id: str, serializer_data):
        serializer = EventSerializerCreate(data=serializer_data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()  # insert Event in db
            return
        if _ID in serializer.errors and len(serializer.errors) == 1:
            # if Event already exists, then update it in db
            assert len(serializer.errors[_ID]) == 1
            assert str(serializer.errors[_ID][0]) == (
                'event with this id already exists.'
            )
            logger.info('event already exists {id}'.format(id=event_id))
            serializer = EventSerializerCreate(
                Event.objects.get(id=event_id),
                data=serializer_data,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()  # update Event in db
        else:
            logger.warning(
                'cannot save event {errors}'.format(errors=serializer.errors),
            )
