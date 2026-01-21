from django.contrib import admin
from .models import Schedule, Attendance
from unfold.admin import ModelAdmin


@admin.register(Schedule)
class ScheduleAdmin(ModelAdmin):
    list_display = ('group',
                    'teacher',
                    'get_day',
                    'start_time',
                    'end_time',
                    'room',
                    'created_at',
                    'updated_at')
    list_filter = ('day_of_week',
                   'teacher',
                   'created_at')
    search_fields = ('group__name',
                     'teacher__user__username',
                     'room')
    readonly_fields = ('created_at',
                       'updated_at')
    fieldsets = (
        ('Schedule',
         {
             'fields': ('group',
                        'teacher',
                        'day_of_week',
                        'start_time',
                        'end_time',
                        'room'),
             }),
        ('Timestamps',
         {
             'fields': ('created_at',
                        'updated_at'),
             'classes': ('collapse',),
             }),
        )

    def get_day( self, obj ):
        return obj.get_day_of_week_display()

    get_day.short_description = 'Day'


@admin.register(Attendance)
class AttendanceAdmin(ModelAdmin):
    list_display = ('student',
                    'get_schedule',
                    'date',
                    'status',
                    'marked_by',
                    'created_at',
                    'updated_at')
    list_filter = ('status',
                   'date',
                   'schedule',
                   'created_at')
    search_fields = ('student__user__username',
                     'student__user__first_name',
                     'student__phone')
    readonly_fields = ('created_at',
                       'updated_at')
    date_hierarchy = 'date'
    fieldsets = (
        ('Attendance',
         {
             'fields': ('schedule',
                        'student',
                        'date',
                        'status'),
             }),
        ('Info',
         {
             'fields': ('marked_by',
                        'notes'),
             }),
        ('Timestamps',
         {
             'fields': ('created_at',
                        'updated_at'),
             'classes': ('collapse',),
             }),
        )

    def get_schedule( self, obj ):
        return f"{obj.schedule.group.name} ({obj.schedule.get_day_of_week_display()})"

    get_schedule.short_description = 'Schedule'
