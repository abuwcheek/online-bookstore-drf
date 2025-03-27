from django.contrib import admin
from .models import CustomUser



@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
     list_display = ['id', 'username', 'first_name', 'last_name', 'gender', 'date_joined', 'is_staff', 'is_active']
     list_display_links = ['id', 'username', 'first_name']
     list_filter = ['gender', 'birth_date', 'is_staff', 'date_joined', 'is_active']
     list_editable = [ 'is_staff', 'is_active']