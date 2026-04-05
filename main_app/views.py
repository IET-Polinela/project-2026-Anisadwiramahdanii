from django.shortcuts import render, redirect
from .models import Report
from .forms import ReportForm


# HOME (dari Lab 2)
def home(request):
    return render(request, 'main_app/home.html')


# CREATE (Tambah laporan)
def add_report(request):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('report_list')
    else:
        form = ReportForm()

    return render(request, 'main_app/add_report.html', {'form': form})


# READ (Tampilkan semua laporan)
def report_list(request):
    reports = Report.objects.all()
    return render(request, 'main_app/report_list.html', {'reports': reports})


# UPDATE (Edit laporan)
def update_report(request, id):
    report = Report.objects.get(id=id)
    form = ReportForm(request.POST or None, instance=report)

    if form.is_valid():
        form.save()
        return redirect('report_list')

    return render(request, 'main_app/add_report.html', {'form': form})


# DELETE (Hapus laporan)
def delete_report(request, id):
    report = Report.objects.get(id=id)
    report.delete()
    return redirect('report_list')

def about(request):
    return render(request, 'main_app/about.html')


def contact(request):
    return render(request, 'main_app/contact.html')