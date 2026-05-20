from rest_framework import serializers

from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    reporter = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            'id',
            'reporter',
            'title',
            'category',
            'description',
            'location',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'reporter', 'created_at', 'updated_at']

    def get_reporter(self, obj):
        return 'Warga Anonim'

    def validate(self, attrs):
        request = self.context.get('request')

        if (
            request
            and request.method in ['PUT', 'PATCH']
            and not request.user.is_admin
            and 'status' in self.initial_data
        ):
            raise serializers.ValidationError({
                'status': 'Status hanya dapat diubah oleh Admin.'
            })

        return attrs
