from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import BootstrapAuthenticationForm, CitizenRegistrationForm


class UserLoginView(LoginView):
    template_name = 'usermanagement_24782037/login.html'
    authentication_form = BootstrapAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, f"Login berhasil. Selamat datang, {form.get_user().username}.")
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Logout berhasil.')
        return super().post(request, *args, **kwargs)


class CitizenRegisterView(CreateView):
    form_class = CitizenRegistrationForm
    template_name = 'usermanagement_24782037/register.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Registrasi berhasil. Silakan login menggunakan akun baru kamu.')
        return super().form_valid(form)
