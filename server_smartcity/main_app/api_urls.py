from rest_framework.routers import DefaultRouter

from .api_views import ReportViewSet


router = DefaultRouter()
router.register(r'reports', ReportViewSet, basename='reports-api')
router.register(r'report', ReportViewSet, basename='report-api')

urlpatterns = router.urls
