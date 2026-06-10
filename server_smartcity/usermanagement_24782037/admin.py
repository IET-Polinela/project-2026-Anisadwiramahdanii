from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role aplikasi', {'fields': ('is_admin', 'is_member')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role aplikasi', {'fields': ('is_admin', 'is_member')}),
    )
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'is_admin', 'is_member')
    list_filter = ('is_staff', 'is_superuser', 'is_admin', 'is_member')
