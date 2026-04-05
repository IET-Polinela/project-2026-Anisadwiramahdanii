from django.urls import path
from . import views

urlpatterns = [
    # dari Lab 2
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # dari Lab 3 (CRUD)
    path('reports/', views.report_list, name='report_list'),
    path('add/', views.add_report, name='add_report'),
    path('update/<int:id>/', views.update_report, name='update_report'),
    path('delete/<int:id>/', views.delete_report, name='delete_report'),
]