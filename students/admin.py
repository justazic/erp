from django.contrib import admin
from .models import Student
import unfold
@admin.register(Student)
class StudentAdmin(unfold.admin.ModelAdmin):
  list_display = ('user', 'phone', 'address', 'active', 'created_at', 'updated_at')
  list_filter = ('active', 'created_at')
  search_fields = ('user__username', 'user__email', 'phone', 'address')
  readonly_fields = ('created_at', 'updated_at')
  fieldsets = (
      ('User Information', {
          'fields': ('user',)
      }),
      ('Contact Information', {
          'fields': ('phone', 'address')
      }),
      ('Status', {
          'fields': ('active',)
      }),
      ('Timestamps', {
          'fields': ('created_at', 'updated_at'),
          'classes': ('collapse',)
      }),
  )

