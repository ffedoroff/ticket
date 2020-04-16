import logging

from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet

from server.apps.main.event.models import Event

logger = logging.getLogger(__name__)


class EventSerializer(serializers.ModelSerializer):
    """Simple Event serializer."""

    # user_id = serializers.IntegerField()
    # sample_section = serializers.JSONField(
    #     default=get_default_sample_section(),
    #     initial=get_default_sample_section(),
    # )

    class Meta(object):
        model = Event
        fields = (
            'created',
            'data',
            'id',
            'modified',
        )
        read_only_fields = (
            'created',
            'modified',
            # 'status',
            # 'status_code',
            # 'status_text',
        )
        # extra_kwargs = {'source_file': {'write_only': True}}

    # def validate_user_id(self, value):  # noqa: WPS110
    #     """Use user permissions from UserViewSet."""
    #     user = UserViewSet(request=self.root.context['request']).get_queryset().filter(pk=value).first()
    #     if not user:
    #         raise serializers.ValidationError('incorrect user_id')
    #     return user.pk
    #
    # def validate_source_file(self, value):  # noqa: WPS110
    #     """Check uploaded file size."""
    #     if value.size < MIN_SOURCE_SIZE:
    #         raise serializers.ValidationError(f'Min file size should be greater than {MIN_SOURCE_SIZE} bytes')
    #     return value
    #
    # def run_parse_job(self, plan):
    #     """Clean previous results and run kubernetes job to parse PDF file."""
    #     assert plan.status_code in {Plan.Status.ERROR, Plan.Status.COMPLETED}
    #     logger.info(f'run_parse_job plan_pk:{plan.pk} plan_version:{plan.version}')
    #     plan.status_code = Plan.Status.PROCESSING
    #     for sample_section in plan.sample_section.values():
    #         sample_section['parsed_value'] = None
    #     plan.reports = None
    #     plan.status = {
    #         'started': timezone.now().isoformat(),
    #         'percent': 0,
    #     }
    #     plan.update_status(description='Starting...')
    #     plan.save()
    #     PlanParseView().run_job(plan_id=plan.pk, plan_version=plan.version)


#
# class PlanCreate(PlanBaseSerializer):
#     """Create plan."""
#
#     def create(self, validated_data):
#         """Create new plan."""
#         validated_data.pop('sample_section', None)
#         instance = super().create(validated_data)
#         self.run_parse_job(instance)
#         return instance
#
#
# class PlanUpdate(PlanBaseSerializer):
#     """Update plan."""
#
#     source_file = serializers.FileField(write_only=True, required=False)
#
#     def update(self, instance, validated_data):
#         """Update plan."""
#         if instance.status_code not in {Plan.Status.ERROR, Plan.Status.COMPLETED}:
#             raise ParseError(f'Plan is read-only when status_code={instance.status_code}')
#         if 'source_file' in validated_data:
#             logger.info('New file uploaded, reset sample_section')
#             validated_data['sample_section'] = get_default_sample_section()
#         validated_data.pop('user_id')  # user_id is readonly
#         instance = super().update(instance, validated_data)
#         self.run_parse_job(instance)
#         return instance


class EventViewSet(ModelViewSet):
    """Simple Plan ViewSet CRUD."""

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_fields = (
        'status_code',
        'user_id',
    )
    ordering = ('created',)

    # @action(detail=True, methods=['GET'], url_path='download-all')
    # def download_all(self, request, pk):
    #     """Endpoint for downloading archive of result files."""
    #     plan = self.get_object()
    #     plan_created = plan.created.strftime('%Y-%m-%d')
    #     plan_files = plan.reports
    #     zip_archive_name = f'plans_{plan_created}.zip'
    #     buffer = BytesIO()
    #     with zipfile.ZipFile(buffer, 'w') as new_archive:
    #         for plan_file in plan_files['files']:
    #             with default_storage.open(plan_file['storage_name']) as file_handler:
    #                 new_archive.writestr(plan_file['name'], file_handler.read())
    #     response = HttpResponse(buffer.getvalue(), content_type='application/zip')
    #     response['Content-Disposition'] = f'attachment; filename="{zip_archive_name}"'
    #     return response
