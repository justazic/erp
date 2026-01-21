from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import TeacherCourse

@admin.register(TeacherCourse)
class ModelNameAdmin(ModelAdmin):
  list_display = ('teacher', 'course')
  list_filter = ('teacher', 'course')
  search_fields = ('teacher', 'course')