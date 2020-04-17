from django.contrib.postgres.fields import JSONField
from django.db import models
from typing_extensions import Final, final

from server.json_tools import DecimalJSONEncoder

#: That's how constants should be defined.
_ID_MAX_LENGTH: Final = 120
_TEXT_MAX_LENGTH: Final = 240

# event name, event start date, promoter name,
# ticket cost (min and max for a standard price).


@final
class Event(models.Model):
    """Main Event model."""

    id = models.CharField(  # noqa: WPS125
        help_text='source: id',
        primary_key=True,
        max_length=_ID_MAX_LENGTH,
    )
    name = models.CharField(
        help_text='source: name',
        max_length=_TEXT_MAX_LENGTH,
    )
    start_date = models.DateTimeField(
        help_text='source: dates.start.dateTime',
    )
    promoter_name = models.CharField(
        help_text='source: promoter.name',
        max_length=_TEXT_MAX_LENGTH,
    )
    cost_min = models.DecimalField(
        help_text='source: priceRanges.min',
        max_digits=10,
        decimal_places=2,
    )
    cost_max = models.DecimalField(
        help_text='source: priceRanges.max',
        max_digits=10,
        decimal_places=2,
    )
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    data = JSONField(  # noqa: WPS110
        help_text='raw json data',
        encoder=DecimalJSONEncoder,
    )

    def __str__(self) -> str:
        """All django models should have this method."""
        return self.id
