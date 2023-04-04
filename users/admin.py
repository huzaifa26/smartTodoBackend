from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserAdmin(admin.ModelAdmin):
    list_filter = ('is_staff',)

admin.site.register(CustomUser, CustomUserAdmin)