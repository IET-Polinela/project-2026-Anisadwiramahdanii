from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', include('about.urls')),
    path('contact/', include('contacts.urls')),
    path('', include('main_app.urls')),
]
