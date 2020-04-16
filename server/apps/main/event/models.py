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

    created = models.DateTimeField(auto_now_add=True)
    data = JSONField(  # noqa: WPS110
        help_text='raw json data',
        encoder=DecimalJSONEncoder,
    )
    id = models.CharField(  # noqa: WPS125
        help_text='source: id',
        primary_key=True,
        max_length=_ID_MAX_LENGTH,
    )
    modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """All django models should have this method."""
        return self.id
