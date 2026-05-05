from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('24782037_iet_2026.usermanagement_24782037.urls')),
    path('dashboard/', include('24782037_iet_2026.dashboard_24782037.urls')),
    path('about/', include('about.urls')),
    path('contact/', include('contacts.urls')),
    path('', include('main_app.urls')),
]
