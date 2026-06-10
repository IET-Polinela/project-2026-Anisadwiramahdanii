from django import forms

from .models import Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reporter_name', 'title', 'category', 'description', 'location']
        widgets = {
            'reporter_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Masukkan nama pelapor'}
            ),
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Contoh: Lampu jalan mati'}
            ),
            'category': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Contoh: Infrastruktur'}
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Jelaskan masalah yang ditemukan secara singkat dan jelas.',
                }
            ),
            'location': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Contoh: Jl. Merdeka No. 10'}
            ),
        }
