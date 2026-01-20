from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'active')
    list_filter = ('active',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
