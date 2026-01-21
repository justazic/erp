from django.contrib import admin
from .models import Assignment, Submission
from unfold.admin import ModelAdmin


@admin.register(Assignment)
class AssignmentAdmin(ModelAdmin):
  list_display = ('title',
                  'teacher',
                  'group',
                  'status',
                  'deadline',
                  'created_at',
                  'updated_at')
  list_filter = ('teacher',
                 'group',
                 'status',
                 'deadline',
                 'created_at')
  search_fields = ('title',
                   'description',
                   'teacher__username',
                   'group__name')
  readonly_fields = ('created_at',
                     'updated_at')
  fieldsets = (
    ('Assignment',
     {
       'fields': ('title',
                  'description',
                  'teacher',
                  'group'),
       }),
    ('Details',
     {
       'fields': ('status',
                  'deadline'),
       }),
    ('Timestamps',
     {
       'fields': ('created_at',
                  'updated_at'),
       'classes': ('collapse',),
       }),
    )


@admin.register(Submission)
class SubmissionAdmin(ModelAdmin):
  list_display = ('student',
                  'assignment',
                  'status',
                  'grade',
                  'created_at',
                  'updated_at')
  list_filter = ('status',
                 'assignment__teacher',
                 'created_at')
  search_fields = ('student__username',
                   'assignment__title')
  readonly_fields = ('created_at',
                     'updated_at')
  fieldsets = (
    ('Submission',
     {
       'fields': ('assignment',
                  'student',
                  'file'),
       }),
    ('Grading',
     {
       'fields': ('status',
                  'grade',
                  'comment'),
       }),
    ('Timestamps',
     {
       'fields': ('created_at',
                  'updated_at'),
       'classes': ('collapse',),
       }),
    )
