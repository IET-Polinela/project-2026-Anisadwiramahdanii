from django.db.models import Q
from rest_framework import pagination, permissions, viewsets

from .models import Report
from .permissions import IsAdminStatusOnlyOrOwnerAndDraft, IsCitizen
from .serializers import ReportSerializer


class ReportPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.order_by('-updated_at')
    serializer_class = ReportSerializer
    pagination_class = ReportPagination

    def get_queryset(self):
        queryset = Report.objects.order_by('-updated_at')
        user = self.request.user
        tab = self.request.query_params.get('tab')

        if not user or not user.is_authenticated:
            return Report.objects.none()

        if tab == 'my_reports':
            return queryset.filter(reporter=user)

        if tab == 'feed':
            return queryset.exclude(reporter=user).exclude(status='DRAFT')

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
            status=serializer.validated_data.get('status', 'DRAFT'),
        )
