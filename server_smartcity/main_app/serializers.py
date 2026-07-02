from rest_framework import serializers

from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    reporter = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            'id',
            'reporter',
            'is_owner',
            'title',
            'category',
            'description',
            'location',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'reporter', 'created_at', 'updated_at']

    def get_reporter(self, obj) -> str:
        return 'Warga Anonim'

    def get_is_owner(self, obj) -> bool:
        request = self.context.get('request')
        return bool(
            request
            and request.user.is_authenticated
            and obj.reporter_id == request.user.id
        )

    def validate(self, attrs):
        request = self.context.get('request')
        status = attrs.get('status')

        if (
            request
            and request.method in ['POST', 'PUT', 'PATCH']
            and not request.user.is_admin
            and status
        ):
            instance = getattr(self, 'instance', None)
            is_owner_draft = (
                instance
                and instance.reporter_id == request.user.id
                and instance.status == 'DRAFT'
            )
            is_new_report = instance is None

            if status not in ['DRAFT', 'REPORTED'] or not (is_new_report or is_owner_draft):
                raise serializers.ValidationError({
                    'status': 'Citizen hanya dapat menyimpan draft atau mengajukan draft miliknya.'
                })

        return attrs
