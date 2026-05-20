from importlib import import_module

from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

RegisterView = import_module(
    'usermanagement_24782037.api_views'
).RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', RegisterView.as_view(), name='api-register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('main_app.api_urls')),
    path('accounts/', include('usermanagement_24782037.urls')),
    path('dashboard/', include('dashboard_24782037.urls')),
    path('about/', include('about.urls')),
    path('contact/', include('contacts.urls')),
    path('', include('main_app.urls')),
]
