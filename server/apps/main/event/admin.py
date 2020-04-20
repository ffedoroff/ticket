
from django.contrib import admin  # noqa: F401

# Register your models here.
from server.apps.main.event.models import Event


@admin.register(Event)
class PlanAdmin(admin.ModelAdmin):
    """Simple admin for Event."""

    list_display = (
        'id',
        'name',
        'start_date',
        'promoter_name',
        'cost_min',
        'cost_max',
        'created',
        'modified',
    )
    list_filter = ('start_date', 'created', 'modified')
