from django.contrib.postgres.fields import JSONField
from django.db import models
from typing_extensions import Final, final

from server.json_tools import DecimalJSONEncoder

#: That's how constants should be defined.
_ID_MAX_LENGTH: Final = 120
_TEXT_MAX_LENGTH: Final = 240

# 4. Inside your Django app, create a searchable api endpoint (returns json) allow the api request to search for
# event name, event start date, promoter name, ticket cost (min and max for a standard price).


@final
class Event(models.Model):
    id = models.CharField(help_text='source: id', primary_key=True, max_length=_ID_MAX_LENGTH)
    # name = models.CharField(max_length=_TEXT_MAX_LENGTH)
    # start = models.DateTimeField(help_text='source: dates.start.dateTime')
    # promoter_name = models.CharField(help_text='source: promoter.name' max_length=_POST_TITLE_MAX_LENGTH)
    data = JSONField(help_text='raw json data', encoder=DecimalJSONEncoder)
    # cost_standard_min = models.

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """All django models should have this method."""
        return self.id
