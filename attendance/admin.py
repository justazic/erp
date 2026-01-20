from django.contrib import admin
import unfold
from .models import Attendance

class AttendanceAdmin(unfold.admin.ModelAdmin):
  list_display = ['student', 'status', 'created_at', 'updated_at']
  search_fields = ['student__user__username', 'student__phone']
  list_filter = ['status']
  date_hierarchy = 'created_at'
  ordering = ['-created_at']
  readonly_fields = ['created_at', 'updated_at']
  fieldsets = (
    (None,
     {
       "fields": ("student", "updated_at", "status")
     }),
  )


admin.site.register(Attendance, AttendanceAdmin)