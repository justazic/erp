from django.contrib import admin
from .models import Course, Group, Comment
import unfold

class CourseAdmin(unfold.admin.ModelAdmin):
  list_display = ('name', 'created_at', 'updated_at')
  search_fields = ('name',)
  ordering = ('name',)
  readonly_fields = ('created_at', 'updated_at')
  fieldsets = (
      ('Course Information', {
          'fields': ('name',)
      }),
      ('Timestamps', {
          'fields': ('created_at', 'updated_at'),
          'classes': ('collapse',)
      }),
  )


class GroupAdmin(unfold.admin.ModelAdmin):
  list_display = ('name', 'course', 'teacher', 'created_at', 'updated_at')
  search_fields = ('name', 'course__name', 'teacher__user__username')
  list_filter = ('course', 'created_at')
  ordering = ('name',)
  readonly_fields = ('created_at', 'updated_at')
  fieldsets = (
      ('Group Information', {
          'fields': ('name', 'course', 'teacher')
      }),
      ('Timestamps', {
          'fields': ('created_at', 'updated_at'),
          'classes': ('collapse',)
      }),
  )


class CommentAdmin(unfold.admin.ModelAdmin):
  list_display = ('user', 'text', 'created_at', 'updated_at')
  search_fields = ('user__username', 'text')
  list_filter = ('created_at',)
  ordering = ('-created_at',)
  readonly_fields = ('created_at', 'updated_at')
  fieldsets = (
      ('Comment Information', {
          'fields': ('user', 'text')
      }),
      ('Timestamps', {
          'fields': ('created_at', 'updated_at'),
          'classes': ('collapse',)
      }),
  )


admin.site.register(Course, CourseAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentAdmin)
