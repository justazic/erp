from django.contrib import admin
from .models import Enrollment
from unfold.admin import ModelAdmin


@admin.register(Enrollment)
class EnrollmentAdmin(ModelAdmin):
    list_display = ('student',
                    'course',
                    'session',
                    'status',
                    'grade',
                    'last_attended',
                    'created_at',
                    'updated_at')
    search_fields = ('student__username',
                     'course__name',
                     'session__session_type')
    list_filter = ('status',
                   'session',
                   'created_at')
    readonly_fields = ('created_at',
                       'updated_at')
    fieldsets = (
        ('Enrollment',
         {
             'fields': ('student',
                        'course',
                        'session'),
             }),
        ('Performance',
         {
             'fields': ('status',
                        'grade',
                        'last_attended'),
             }),
        ('Timestamps',
         {
             'fields': ('created_at',
                        'updated_at'),
             'classes': ('collapse',),
             }),
        )
