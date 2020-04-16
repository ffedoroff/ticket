
from django.contrib import admin  # noqa: F401

# Register your models here.
from server.apps.main.event.models import Event


@admin.register(Event)
class PlanAdmin(admin.ModelAdmin):
    """Simple admin for Event."""

    list_display = (
        'id',
        'created',
        'modified',
    )
    list_filter = ('created', 'modified')
