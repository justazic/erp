from django.contrib import admin
from .models import Course, Group, Comment, Category, Session
from unfold.admin import ModelAdmin


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name',
                    'created_at',
                    'updated_at')
    search_fields = ('name',)
    readonly_fields = ('created_at',
                       'updated_at')
    fieldsets = (
        ('Info',
         {
             'fields': ('name',),
             }),
        ('Timestamps',
         {
             'fields': ('created_at',
                        'updated_at'),
             'classes': ('collapse',),
             }),
        )


@admin.register(Course)
class CourseAdmin(ModelAdmin):
    list_display = ('name',
                    'category',
                    'price',
                    'created_at',
                    'updated_at')
    search_fields = ('name',
                     'small_description',
                     'large_description')
    list_filter = ('category',
                   'created_at')
    readonly_fields = ('created_at',
                       'updated_at')
    fieldsets = (
        ('Info',
         {
             'fields': ('name',
                        'category',
                        'price'),
             }),
        ('Description',
         {
             'fields': ('small_description',
                        'large_description'),
             }),
        ('Images',
         {
             'fields': ('small_image',
                        'large_image'),
             }),
        ('Timestamps',
         {
             'fields': ('created_at',
                        'updated_at'),
             'classes': ('collapse',),
             }),
        )


@admin.register(Session)
class SessionAdmin(ModelAdmin):
    list_display = ('course',
                    'session_type',
                    'start_date',
                    'end_date',
                    'capacity',
                    'is_active',
                    'created_at',
                    'updated_at')
    search_fields = ('course__name',
                     'session_type')
    list_filter = ('session_type',
                   'is_active',
                   'created_at')
    readonly_fields = ('created_at',
                       'updated_at')
    fieldsets = (
        ('Session',
         {
             'fields': ('course',
                        'session_type'),
             }),
        ('Duration',
         {
             'fields': ('start_date',
                        'end_date'),
             }),
        ('Capacity',
         {
             'fields': ('capacity',
                        'is_active'),
             }),
        ('Timestamps',
         {
             'fields': ('created_at',
                        'updated_at'),
             'classes': ('collapse',),
             }),
        )


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    list_display = ('name',
                    'course',
                    'session',
                    'teacher',
                    'created_at',
                    'updated_at')
    search_fields = ('name',
                     'course__name',
                     'session__session_type',
                     'teacher__user__username')
    list_filter = ('course',
                   'session',
                   'teacher',
                   'created_at')
    readonly_fields = ('created_at',
                       'updated_at')
    fieldsets = (
        ('Info',
         {
             'fields': ('name',
                        'course',
                        'session',
                        'teacher'),
             }),
        ('Timestamps',
         {
             'fields': ('created_at',
                        'updated_at'),
             'classes': ('collapse',),
             }),
        )


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ('user',
                    'text',
                    'created_at',
                    'updated_at')
    search_fields = ('user__username',
                     'text')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',
                       'updated_at')
    fieldsets = (
        ('Comment',
         {
             'fields': ('user',
                        'text'),
             }),
        ('Timestamps',
         {
             'fields': ('created_at',
                        'updated_at'),
             'classes': ('collapse',),
             }),
        )
