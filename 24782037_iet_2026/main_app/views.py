from django.http import HttpResponseBadRequest
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Report, STATUS_CHOICES
from .forms import ReportStatusForm

# ======================
# HOME (HALAMAN UTAMA)
# ======================
class HomeView(ListView):
    model = Report
    template_name = 'main_app/home.html'
    context_object_name = 'reports'


# ======================
# LIST (OPSIONAL)
# ======================
class ReportListView(ListView):
    model = Report
    template_name = 'main_app/report_list.html'
    context_object_name = 'reports'


# ======================
# DETAIL
# ======================
class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_form'] = ReportStatusForm(instance=self.object)
        context['status_history'] = self.object.status_changes.all()
        return context


# ======================
# CREATE
# ======================
class ReportCreateView(CreateView):
    model = Report
    fields = ['reporter_name', 'title', 'category', 'description', 'location']  # 🔥 FIX
    template_name = 'main_app/report_form.html'
    success_url = reverse_lazy('home')


# ======================
# UPDATE
# ======================
class ReportUpdateView(UpdateView):
    model = Report
    fields = ['reporter_name', 'title', 'category', 'description', 'location']  # 🔥 FIX
    template_name = 'main_app/report_form.html'
    success_url = reverse_lazy('home')


# ======================
# DELETE
# ======================
class ReportDeleteView(DeleteView):
    model = Report
    template_name = 'main_app/report_confirm_delete.html'
    success_url = reverse_lazy('home')


# ======================
# WORKFLOW STATUS
# ======================
class ReportUpdateStatusView(View):
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        form = ReportStatusForm(request.POST, instance=report)
        if form.is_valid():
            old_status = report.status
            new_status = form.cleaned_data['status']
            form.save()
            if old_status != new_status:
                report.status_changes.create(
                    old_status=old_status,
                    new_status=new_status,
                    note=f"Perubahan status dari {dict(STATUS_CHOICES)[old_status]} ke {dict(STATUS_CHOICES)[new_status]}"
                )
            return redirect('report_detail', pk=report.pk)
        return HttpResponseBadRequest('Status tidak valid.')