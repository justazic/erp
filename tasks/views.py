from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Q
from .models import Assignment, Submission
from courses.models import Group



class AssigmentCreateView(LoginRequiredMixin, View):
  def get( self, request, group_id=None ):
    if request.user.role not in ['teacher', 'admin']:
      return redirect('/')

    if request.user.role == 'admin':
      groups = Group.objects.all()
    else:
      groups = Group.objects.filter(teacher=request.user)

    selected_group = None
    if group_id:
      selected_group = get_object_or_404(Group, id=group_id)

    schedule_id = request.GET.get('schedule_id')

    return render(request, 'tasks/assignment_create.html', {
      'groups': groups,
      'selected_group': selected_group,
      'schedule_id': schedule_id,
    })

  def post( self, request, group_id=None ):
    if request.user.role not in ['teacher', 'admin']:
      return redirect('/')

    schedule_id = request.POST.get('schedule_id')

    Assignment.objects.create(
      teacher=request.user,
      title=request.POST.get('title'),
      description=request.POST.get('description'),
      deadline=request.POST.get('deadline'),
      group_id=request.POST.get('group'),
      schedule_id=schedule_id if schedule_id else None,
      status='published'
      )

    if schedule_id:
      return redirect('attendance:schedule_detail', schedule_id=schedule_id)

    return redirect('tasks:assignment_list')


class AssigmentListView(LoginRequiredMixin, View):
  def get( self, request ):
    search = request.GET.get('search', '')
    if request.user.role == 'teacher':
      assignments = Assignment.objects.filter(teacher=request.user)
    elif request.user.role == 'student':
      student_groups = Group.objects.filter(course__enrollments__student=request.user)
      assignments = Assignment.objects.filter(group__in=student_groups)
    else:
      assignments = Assignment.objects.all()

    if search:
        assignments = assignments.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(group__name__icontains=search)
        )

    return render(request, 'tasks/assignment_list.html', {
      'assignments': assignments,
      'search': search,
      }
                  )


class SubmissionCreateView(LoginRequiredMixin, View):
  def get( self, request, assignment_id ):
    if request.user.role != 'student':
      return redirect('/')

    assignment = get_object_or_404(Assignment, id=assignment_id)

    if assignment.is_expired():
      return render(request, 'tasks/deadline_expired.html', {
        'assignment': assignment
        }
                    )

    return render(request, 'tasks/submission_create.html', {
      'assignment': assignment
      }
                  )

  def post( self, request, assignment_id ):
    if request.user.role != 'student':
      return redirect('/')
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if assignment.is_expired():
      return redirect('/tasks/assignments/')

    Submission.objects.create(
      assignment_id=assignment_id,
      student=request.user,
      file=request.FILES[ 'file' ],
      comment=request.POST.get('comment', '')
      )
    return redirect('/tasks/my-submissions/')


class MySubmissionListView(LoginRequiredMixin, View):
  def get( self, request ):
    if request.user.role != 'student':
      return redirect('/')
    submissions = Submission.objects.filter(student=request.user)
    return render(request, 'tasks/my_submissions.html', {
      'submissions': submissions
      }
                  )


class SubmissionsListTeacherView(LoginRequiredMixin, View):
  def get( self, request, assignment_id ):
    if request.user.role != 'teacher':
      return redirect('/')

    assignment = get_object_or_404(Assignment, id=assignment_id, teacher=request.user)
    submissions = Submission.objects.filter(assignment=assignment)
    return render(request, 'tasks/submission_list_teacher.html', {
      'assignment': assignment,
      'submissions': submissions
      }
                  )


class SubmissionCheckView(LoginRequiredMixin, View):
  def post( self, request, submission_id ):
    if request.user.role != 'teacher':
      return redirect('/')
    submission = get_object_or_404(Submission, id=submission_id, assignment__teacher=request.user)
    submission.grade = request.POST.get('grade')
    submission.status = 'graded'
    submission.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))


class AssigmentUpdateView(LoginRequiredMixin, View):
  def get( self, request, assignment_id ):
    if request.user.role not in ['teacher', 'admin']:
      return redirect('/')

    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.user.role == 'teacher' and assignment.teacher != request.user:
      return redirect('/')

    if request.user.role == 'admin':
      groups = Group.objects.all()
    else:
      groups = Group.objects.filter(teacher=request.user)

    return render(request, 'tasks/assignment_edit.html', {
      'assignment': assignment,
      'groups': groups
    })

  def post( self, request, assignment_id ):
    if request.user.role not in ['teacher', 'admin']:
      return redirect('/')

    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.user.role == 'teacher' and assignment.teacher != request.user:
      return redirect('/')

    assignment.title = request.POST.get('title')
    assignment.description = request.POST.get('description')
    assignment.deadline = request.POST.get('deadline')
    assignment.group_id = request.POST.get('group')
    assignment.save()
    return redirect(request.META.get('HTTP_REFERER', '/tasks/assignments/'))


class AssigmentDeleteView(LoginRequiredMixin, View):
  def post( self, request, assignment_id ):
    if request.user.role not in ['teacher', 'admin']:
      return redirect('/')
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.user.role == 'teacher' and assignment.teacher != request.user:
      return redirect('/')
    assignment.delete()
    return redirect('/tasks/assignments/')