from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reporter_name', 'title', 'category', 'description', 'location']

        widgets = {
            'reporter_name': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ReportStatusForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'})
        }
        labels = {
            'status': 'Status Validasi'
        }