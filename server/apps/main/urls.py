from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from server.apps.main.event.views import EventViewSet

app_name = 'main'

router = routers.DefaultRouter()
router.register(r'event', EventViewSet, basename='event')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include((router.urls, app_name), namespace='drf'), name='index'),
]
