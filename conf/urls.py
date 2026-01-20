from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include

from students.models import Student
from teachers.models import Teacher

from datetime import date

def years_between():
  start_date = date(2010, 6, 15)
  end_date = date.today()
  years = end_date.year - start_date.year
  if (end_date.month, end_date.day) < (start_date.month, start_date.day):
    years -= 1
  return years


def index( request ):
  number_of_students = Student.objects.count()
  graduated_percentage = int(Student.objects.filter(status='graduated').count() / number_of_students * 100)
  currently_studying_percentage = int(Student.objects.filter(status='studying').count() / number_of_students * 100)
  experts = Teacher.objects.filter(is_expert=True).count()
  return render(request, 'index.html', {
    'number_of_students': number_of_students,
    'graduated_percentage': graduated_percentage,
    'currently_studying_percentage': currently_studying_percentage,
    'experts': experts,
    'years_between': years_between()
    },)


urlpatterns = [ path('admin/', admin.site.urls), path('', index, name='index'),
  path('accounts/', include('accounts.urls')), path('students/', include('students.urls')),
  path('teachers/', include('teachers.urls')), path('tasks/', include('tasks.urls')),
  path('attendance/', include('attendance.urls')), path('finance/', include('finance.urls')),
  path('courses/', include('courses.urls')), ]

# Serve media and static files in development
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

