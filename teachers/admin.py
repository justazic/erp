from django.contrib import admin
from .models import Teacher
import unfold

@admin.register(Teacher)
class TeacherAdmin(unfold.admin.ModelAdmin):
  list_display = ('user', 'speciality', 'created_at', 'updated_at')
  search_fields = ('user__username', 'user__email', 'speciality')
  ordering = ('user__username',)
  readonly_fields = ('created_at', 'updated_at')
  fieldsets = (
      ('User Information', {
          'fields': ('user',)
      }),
      ('Professional Information', {
          'fields': ('speciality',)
      }),
      ('Timestamps', {
          'fields': ('created_at', 'updated_at'),
          'classes': ('collapse',)
      }),
  )

