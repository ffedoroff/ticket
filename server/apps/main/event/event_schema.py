# flake8: noqa
EVENT_SCHEMA = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'id': {'type': 'string'},
        'dates': {
            'type': 'object',
            'properties': {
                'start': {
                    'type': 'object',
                    'properties': {'dateTime': {'type': 'string'}},
                    'required': ['dateTime'],
                },
            },
            'required': ['start'],
        },
        'promoter': {
            'type': 'object',
            'properties': {'name': {'type': 'string'}},
            'required': ['name'],
        },
        'priceRanges': {
            'type': 'array',
            'items': [
                {
                    'type': 'object',
                    'properties': {
                        'type': {'type': 'string'},
                        'currency': {'type': 'string'},
                        'min': {'type': 'number'},
                        'max': {'type': 'number'},
                    },
                    'required': [
                        'type',
                        'currency',
                        'min',
                        'max',
                    ],
                },
            ],
        },
    },
    'required': [
        'name',
        'id',
        'dates',
        'promoter',
        'priceRanges',
    ],
}
