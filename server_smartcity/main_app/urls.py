from django.urls import path

from .views import (
    HomeView,
    ReportCreateView,
    ReportDeleteView,
    ReportDetailView,
    ReportDetailJsonView,
    ReportListView,
    ReportSearchView,
    ReportUpdateStatusView,
    ReportUpdateView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('reports/', ReportListView.as_view(), name='report_list'),
    path('reports/search/', ReportSearchView.as_view(), name='report_search'),
    path('report/<int:pk>/', ReportDetailView.as_view(), name='report_detail'),
    path('report/<int:pk>/json/', ReportDetailJsonView.as_view(), name='report_detail_json'),
    path('report/create/', ReportCreateView.as_view(), name='create_report'),
    path('report/update/<int:pk>/', ReportUpdateView.as_view(), name='update_report'),
    path('report/delete/<int:pk>/', ReportDeleteView.as_view(), name='delete_report'),
    path('report/<int:pk>/status/', ReportUpdateStatusView.as_view(), name='update_status'),
]
