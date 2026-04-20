from django.urls import path

from .views import (
    HomeView,
    ReportCreateView,
    ReportDeleteView,
    ReportDetailView,
    ReportListView,
    ReportUpdateStatusView,
    ReportUpdateView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('reports/', ReportListView.as_view(), name='report_list'),
    path('report/<int:pk>/', ReportDetailView.as_view(), name='report_detail'),
    path('create/', ReportCreateView.as_view(), name='create_report'),
    path('update/<int:pk>/', ReportUpdateView.as_view(), name='update_report'),
    path('delete/<int:pk>/', ReportDeleteView.as_view(), name='delete_report'),
    path('update-status/<int:pk>/', ReportUpdateStatusView.as_view(), name='update_status'),
]
