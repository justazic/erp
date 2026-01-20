from .models import Course
from django.db.models import Count

popular_courses = (
    Course.objects
    .annotate(popularity=Count('enrollments'))
    .order_by('-popularity')[:6]
)