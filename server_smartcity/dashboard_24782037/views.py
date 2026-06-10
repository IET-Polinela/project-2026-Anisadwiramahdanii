from django.db.models import Count
from django.http import JsonResponse
from django.views.generic import TemplateView, View

from main_app.models import Report, STATUS_CHOICES


class DashboardView(TemplateView):
    template_name = 'dashboard_24782037/dashboard.html'


class DashboardDataView(View):
    def get(self, request):
        status_counts = {
            item['status']: item['total']
            for item in Report.objects.values('status').annotate(total=Count('id')).order_by('status')
        }
        status_labels = dict(STATUS_CHOICES)

        category_counts = list(
            Report.objects.values('category')
            .annotate(total=Count('id'))
            .order_by('-total', 'category')
        )

        latest_reported = Report.objects.filter(status='REPORTED').order_by('-created_at')[:5]
        latest_resolved = Report.objects.filter(status='RESOLVED').order_by('-created_at')[:5]

        return JsonResponse({
            'status_distribution': {
                'labels': [status_labels[code] for code, _ in STATUS_CHOICES],
                'data': [status_counts.get(code, 0) for code, _ in STATUS_CHOICES],
            },
            'category_distribution': {
                'labels': [item['category'] for item in category_counts],
                'data': [item['total'] for item in category_counts],
            },
            'latest_reported': [self.serialize_report(report) for report in latest_reported],
            'latest_resolved': [self.serialize_report(report) for report in latest_resolved],
        })

    def serialize_report(self, report):
        return {
            'id': report.id,
            'title': report.title,
            'reporter_name': report.reporter_name,
            'category': report.category,
            'location': report.location,
            'status': report.get_status_display(),
            'created_at': report.created_at.strftime('%d %b %Y, %H:%M'),
        }

