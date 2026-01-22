import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Category, Course, Session, Group
from students.models import Enrollment
from teachers.models import TeacherCourse
from tasks.models import Assignment, Submission
from attendance.models import Schedule, Attendance
from django.utils import timezone
from datetime import timedelta, time

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating database...')

        categories_names = ['Programming', 'Design', 'Marketing', 'Business', 'Music']
        categories = []
        for name in categories_names:
            cat, created = Category.objects.get_or_create(name=name)
            categories.append(cat)
        self.stdout.write(f'Created {len(categories)} categories.')

        teachers = []
        for i in range(1, 11):
            username = f'teacher{i}'
            email = f'teacher{i}@example.com'
            teacher, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'role': 'teacher',
                    'first_name': f'Teacher',
                    'last_name': f'Number {i}',
                    'speciality': random.choice(['Python Specialist', 'UI/UX Designer', 'Digital Marketer', 'Economics Professor', 'Piano Teacher']),
                    'is_expert': random.choice([True, False])
                }
            )
            if created:
                teacher.set_password('password123')
                teacher.save()
            teachers.append(teacher)
        self.stdout.write(f'Created {len(teachers)} teachers.')

        students = []
        for i in range(1, 101):
            username = f'student{i}'
            email = f'student{i}@example.com'
            student, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'role': 'student',
                    'first_name': f'Student',
                    'last_name': f'Number {i}',
                    'balance': random.randint(100, 1000)
                }
            )
            if created:
                student.set_password('password123')
                student.save()
            students.append(student)
        self.stdout.write(f'Created {len(students)} students.')

        course_data = [
            ('Python for Beginners', 'Programming', 99),
            ('Advanced Web Design', 'Design', 149),
            ('SEO Mastery', 'Marketing', 79),
            ('Business Strategy', 'Business', 199),
            ('Music Theory 101', 'Music', 59),
            ('Django Web Framework', 'Programming', 129),
            ('Graphic Design Basics', 'Design', 89),
            ('Social Media Marketing', 'Marketing', 69),
            ('Entrepreneurship', 'Business', 159),
            ('Piano Fundamentals', 'Music', 119),
        ]
        courses = []
        for name, cat_name, price in course_data:
            cat = Category.objects.get(name=cat_name)
            course, created = Course.objects.get_or_create(
                name=name,
                defaults={
                    'category': cat,
                    'price': price,
                    'small_description': f'Learn {name} from scratch.',
                    'large_description': f'This is a comprehensive course about {name}. It covers everything you need to know to get started and succeed in this field.'
                }
            )
            courses.append(course)
            
            TeacherCourse.objects.get_or_create(teacher=random.choice(teachers), course=course)
            
        self.stdout.write(f'Created {len(courses)} courses.')

        sessions = []
        groups = []
        session_types = ['spring', 'summer', 'fall', 'winter']
        
        for course in courses:
            for stype in session_types[:2]:
                session, created = Session.objects.get_or_create(
                    course=course,
                    session_type=stype,
                    defaults={
                        'start_date': timezone.now().date(),
                        'end_date': timezone.now().date() + timedelta(days=90),
                        'capacity': 30,
                        'is_active': True
                    }
                )
                sessions.append(session)
                
                for g_idx in range(1, 3):
                    group, created = Group.objects.get_or_create(
                        name=f'{course.name} - Group {g_idx} ({stype})',
                        course=course,
                        session=session,
                        defaults={
                            'teacher': random.choice(teachers)
                        }
                    )
                    groups.append(group)
        self.stdout.write(f'Created {len(sessions)} sessions and {len(groups)} groups.')

        for student in students:
            enrolled_courses = random.sample(courses, k=random.randint(1, 3))
            for course in enrolled_courses:
                course_sessions = [s for s in sessions if s.course == course]
                if course_sessions:
                    session = random.choice(course_sessions)
                    session_groups = [g for g in groups if g.session == session]
                    group = random.choice(session_groups) if session_groups else None
                    
                    Enrollment.objects.get_or_create(
                        student=student,
                        course=course,
                        defaults={
                            'session': session,
                            'group': group,
                            'status': 'studying'
                        }
                    )
        self.stdout.write('Enrolled students in courses.')

        for group in groups:
            days = random.sample(range(0, 7), k=3)
            times = [time(8, 0), time(10, 0), time(12, 0), time(14, 0), time(16, 0)]
            start_t = random.choice(times)
            end_t = time(start_t.hour + 2, 0)

            for day in days:
                try:
                    Schedule.objects.get_or_create(
                        group=group,
                        day_of_week=day,
                        start_time=start_t,
                        end_time=end_t,
                        defaults={
                            'teacher': group.teacher,
                            'room': f'Room {random.randint(101, 110)}'
                        }
                    )
                except Exception:
                    pass
            
            for i in range(1, 3):
                Assignment.objects.get_or_create(
                    teacher=group.teacher,
                    group=group,
                    title=f'Assignment {i} for {group.name}',
                    defaults={
                        'description': f'Complete the exercises in chapter {i}.',
                        'status': 'published',
                        'deadline': timezone.now() + timedelta(days=7*i)
                    }
                )
        self.stdout.write('Created schedules and assignments.')

        self.stdout.write(self.style.SUCCESS('Successfully populated the database!'))