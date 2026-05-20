from django.db.models import Q
from rest_framework import permissions, viewsets

from .models import Report
from .permissions import IsAdminStatusOnlyOrOwnerAndDraft, IsCitizen
from .serializers import ReportSerializer


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.order_by('-created_at')
    serializer_class = ReportSerializer

    def get_queryset(self):
        queryset = Report.objects.order_by('-created_at')
        user = self.request.user

        if not user or not user.is_authenticated:
            return Report.objects.none()

        if user.is_admin:
            return queryset.exclude(status='DRAFT')

        if user.is_member:
            return queryset.filter(Q(reporter=user) | ~Q(status='DRAFT'))

        return Report.objects.none()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, IsCitizen]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [
                permissions.IsAuthenticated,
                IsAdminStatusOnlyOrOwnerAndDraft,
            ]
        else:
            permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(
            reporter=self.request.user,
            reporter_name='Warga Anonim',
            status='DRAFT',
        )
