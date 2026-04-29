from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ReportForm
from .mixins import AdminRequiredMixin
from .models import Report


class HomeView(ListView):
    model = Report
    template_name = 'main_app/home.html'
    context_object_name = 'reports'

    def get_queryset(self):
        return Report.objects.order_by('-created_at')[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reports = Report.objects.all()
        context['report_count'] = reports.count()
        context['resolved_count'] = reports.filter(status='RESOLVED').count()
        context['verified_count'] = reports.filter(status='VERIFIED').count()
        context['in_progress_count'] = reports.filter(status='IN_PROGRESS').count()
        return context


class ReportListView(ListView):
    model = Report
    template_name = 'main_app/report_list.html'
    context_object_name = 'reports'

    def get_queryset(self):
        queryset = Report.objects.order_by('-created_at')
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(reporter_name__icontains=query)
                | Q(category__icontains=query)
                | Q(location__icontains=query)
                | Q(description__icontains=query)
            )
        return queryset


class ReportSearchView(View):
    def get(self, request):
        query = request.GET.get('q', '').strip()
        reports = Report.objects.order_by('-created_at')

        if query:
            reports = reports.filter(
                Q(title__icontains=query)
                | Q(reporter_name__icontains=query)
                | Q(category__icontains=query)
                | Q(location__icontains=query)
                | Q(description__icontains=query)
            )

        return JsonResponse({
            'query': query,
            'results': [serialize_report(report) for report in reports[:50]],
        })


class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_history'] = self.object.status_changes.all()
        return context


class ReportDetailJsonView(View):
    def get(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        return JsonResponse(serialize_report(report, include_description=True))


class ReportCreateView(AdminRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/report_form.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        messages.success(self.request, 'Laporan baru berhasil ditambahkan.')
        return super().form_valid(form)


class ReportUpdateView(AdminRequiredMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/report_form.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        messages.success(self.request, 'Data laporan berhasil diperbarui.')
        return super().form_valid(form)


class ReportDeleteView(AdminRequiredMixin, DeleteView):
    model = Report
    template_name = 'main_app/report_confirm_delete.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        messages.success(self.request, 'Laporan berhasil dihapus.')
        return super().form_valid(form)


class ReportUpdateStatusView(AdminRequiredMixin, View):
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        next_status = report.next_status
        requested_status = request.POST.get('status')

        if not next_status or requested_status != next_status['value']:
            messages.error(request, 'Perubahan status tidak sesuai alur workflow.')
            return redirect('report_detail', pk=report.pk)

        old_status = report.status
        report.status = requested_status
        report.full_clean()
        report.save(update_fields=['status'])
        report.status_changes.create(
            old_status=old_status,
            new_status=requested_status,
            note=f"Perubahan status dari {dict(report._meta.get_field('status').choices)[old_status]} ke {next_status['label']}",
        )
        messages.success(request, f"Status laporan berhasil diubah ke {next_status['label']}.")
        return redirect('report_detail', pk=report.pk)


def serialize_report(report, include_description=False):
    data = {
        'id': report.id,
        'title': report.title,
        'reporter_name': report.reporter_name,
        'category': report.category,
        'location': report.location,
        'status': report.get_status_display(),
        'status_code': report.status,
        'status_badge_class': report.status_badge_class,
        'created_at': report.created_at.strftime('%d %b %Y, %H:%M'),
        'detail_url': report.get_absolute_url() if hasattr(report, 'get_absolute_url') else '',
    }

    if include_description:
        data['description'] = report.description
        data['status_history'] = [
            {
                'date': change.changed_at.strftime('%d %b %Y, %H:%M'),
                'note': change.note,
                'status': change.get_new_status_display(),
                'status_badge_class': change.new_status_badge_class,
            }
            for change in report.status_changes.all()
        ]
    else:
        data['description'] = report.description[:120]

    return data
