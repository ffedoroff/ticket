# -*- coding: utf-8 -*-

from django.core.serializers.json import DjangoJSONEncoder


class DecimalJSONEncoder(DjangoJSONEncoder):
    """Store decimal as float."""

    def default(self, o):  # noqa: WPS111
        """Decimal rule override."""
        return float(o.normalize())
