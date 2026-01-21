from django.db import models
from accounts.models import User


class Category(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__( self ):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses', blank=True, null=True)
    small_image = models.ImageField(upload_to='courses/small_images', null=True)
    large_image = models.ImageField(upload_to='courses/large_images', null=True)
    small_description = models.TextField(max_length=50)
    large_description = models.TextField(max_length=1000)
    price = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class Session(models.Model):
    SESSION_TYPES = [
        ('1st',
         '1st Session'),
        ('2nd',
         '2nd Session'),
        ('3rd',
         '3rd Session'),
        ('4th',
         '4th Session'),
        ('spring',
         'Spring'),
        ('summer',
         'Summer'),
        ('fall',
         'Fall'),
        ('winter',
         'Winter'),
        ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sessions')
    session_type = models.CharField(max_length=20, choices=SESSION_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    capacity = models.PositiveIntegerField(default=30)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__( self ):
        return f"{self.course.name} - {self.get_session_type_display()}"

    class Meta:
        ordering = ('course',
                    'session_type')
        verbose_name = 'Session'
        verbose_name_plural = 'Sessions'
        unique_together = ('course',
                           'session_type')


class Group(models.Model):
    name = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='groups')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='groups', null=True, blank=True)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='taught_groups',
                                limit_choices_to={
                                    'role': 'teacher',
                                    },
                                )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
        unique_together = ('course',
                           'name')
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
        unique_together = ('course',
                           'name')


class Comment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    rating = models.PositiveIntegerField(default=0)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

