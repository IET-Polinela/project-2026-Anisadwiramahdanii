from django.contrib import messages
from django.shortcuts import redirect


class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            messages.error(request, 'Silakan login terlebih dahulu untuk mengakses fitur admin.')
            return redirect('login')

        if not getattr(user, 'is_admin', False):
            messages.error(request, 'Akses ditolak. Fitur ini hanya untuk admin.')
            return redirect('report_list')

        return super().dispatch(request, *args, **kwargs)
