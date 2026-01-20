from django.contrib import admin
from .models import Student, Enrollment
import unfold

@admin.register(Student)
class StudentAdmin(unfold.admin.ModelAdmin):
  class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0


  list_display = ('user', 'phone', 'address', 'created_at', 'updated_at')
  search_fields = ('user__username', 'user__email', 'phone', 'address')
  readonly_fields = ('created_at', 'updated_at')
  ordering = ('-created_at',)
  inlines = [EnrollmentInline]
  fieldsets = (
      ('User Information', {
          'fields': ('user',)
      }),
      ('Contact Information', {
          'fields': ('phone', 'address')
      }),
      ('Timestamps', {
          'fields': ('created_at', 'updated_at'),
          'classes': ('collapse',)
      }),
  )


@admin.register(Enrollment)
class EnrollmentAdmin(unfold.admin.ModelAdmin):
  list_display = ('student', 'course', 'status','created_at', 'updated_at')
  search_fields = ('student__user__username', 'course__name')
  list_filter = ('created_at',)
  ordering = ('-created_at',)
  readonly_fields = ('created_at', 'updated_at')
  fieldsets = (
      ('Enrollment Information', {
          'fields': ('student', 'course')
      }),
      ('Status', {
          'fields': ('status',)
      }),
      ('Timestamps', {
          'fields': ('created_at', 'updated_at'),
          'classes': ('collapse',)
      })
  )