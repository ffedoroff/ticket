# -*- coding: utf-8 -*-

import decimal

from django.core.serializers.json import DjangoJSONEncoder


class DecimalJSONEncoder(DjangoJSONEncoder):
    """Store decimal as float."""

    def default(self, o):  # noqa: WPS111
        """Decimal rule override."""
        if isinstance(o, decimal.Decimal):
            return float(o.normalize())
        return super().default(o)
