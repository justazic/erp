from django.contrib import admin
from .models import Group #, Course, Comment
# Register your models here.

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'teacher')

# admin.site.register(Course)
# admin.site.register(Comment)