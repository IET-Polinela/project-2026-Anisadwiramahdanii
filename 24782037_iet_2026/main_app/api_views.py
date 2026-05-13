from rest_framework import viewsets

from .models import Report
from .serializers import ReportSerializer


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.order_by('-created_at')
    serializer_class = ReportSerializer

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(reporter=user, reporter_name='Warga Anonim')
