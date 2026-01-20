from django.contrib import admin
from .models import Assignment, Submission
import unfold

@admin.register(Assignment)
class AssignmentAdmin(unfold.admin.ModelAdmin):
    list_display = ('title', 'teacher', 'deadline')
    list_filter = ('teacher',)

@admin.register(Submission)
class SubmissionAdmin(unfold.admin.ModelAdmin):
    list_display = ('assignment', 'student', 'grade', 'checked')
    list_filter = ('checked',)