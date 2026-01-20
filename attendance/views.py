from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from courses.models import Group
from students.models import Student
from .models import Attendance


class AttendanceCreateView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role not in [ 'admin', 'teacher' ]:
            return redirect('/')

        students = Student.objects.select_related('group')
        return render(request, 'attendance/form.html', {
            'students': students,
            },
                      )

    def post(self, request):
        if request.user.role not in [ 'admin', 'teacher' ]:
            return redirect('/')

        today = date.today()
        students = Student.objects.all()

        for student in students:
            status = request.POST.get(f'status_{student.id}')
            if not status:
                continue

            Attendance.objects.update_or_create(
                student=student,
                date=today,
                defaults={
                    'status': status,
                    'marked_by': request.user,
                    },
                )

        return redirect('/attendance/list/')


class AttendanceListView(LoginRequiredMixin, View):
    def get( self, request ):
        if request.user.role not in [ 'admin', 'teacher' ]:
            return redirect('/')

        attendances = Attendance.objects.select_related(
            'student',
            'student__group',
            'marked_by',
            )
        student_id = request.GET.get('student')
        group_id = request.GET.get('group')
        status = request.GET.get('status')
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        if student_id:
            attendances = attendances.filter(student_id=student_id)
        if group_id:
            attendances = attendances.filter(student__group_id=group_id)
        if status:
            attendances = attendances.filter(status=status)
        if date_from:
            attendances = attendances.filter(date__gte=date_from)
        if date_to:
            attendances = attendances.filter(date__lte=date_to)
        attendances = attendances.order_by('-updated_at')

        total_attendance = attendances.count()
        total_present = attendances.filter(status='present').count()
        total_absent = attendances.filter(status='absent').count()

        avg_attendance = int((total_present / total_attendance) * 100) if total_attendance else 0

        context = {
            'attendances': attendances,
            'total_attendance': total_attendance,
            'total_present': total_present,
            'total_absent': total_absent,
            'avg_attendance': avg_attendance,
            'students': Student.objects.all(),
            'groups': Group.objects.all(),
            }

        return render(request, 'attendance/attendance_history.html', context)
