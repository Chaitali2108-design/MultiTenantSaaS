from django.contrib import admin
from .models import User

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'organization', 'is_staff')
    list_filter = ('organization', 'is_staff')
    search_fields = ('username', 'email')

admin.site.register(User, CustomUserAdmin)