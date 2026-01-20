from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from .models import Assignment, Submission
from teachers.models import Teacher
from students.models import Student


# Create your views here.

class AssigmentCreateView(LoginRequiredMixin, View):
  def get( self, request ):
    if request.user.role != 'teacher':
      return redirect('/')

    return render(request, 'tasks/assignment_create.html')

  def post( self, request ):
    if request.user.role != 'teacher':
      return redirect('/')

    Assignment.objects.create(
      teacher=request.user.teacher,
      title=request.POST.get('title'),
      description=request.POST.get('description'),
      deadline=request.POST.get('deadline')
      )
    return redirect('/tasks/assignments/')


class AssigmentListView(LoginRequiredMixin, View):
  def get( self, request ):
    if request.user.role == 'teacher':
      assignments = Assignment.objects.filter(teacher=request.user.teacher)
    else:
      assignments = Assignment.objects.all()
    return render(request, 'tasks/assignment_list.html', {
      'assignments': assignments
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
      student=request.user.student,
      file=request.FILES[ 'file' ],
      comment=request.POST.get('comment', '')
      )
    return redirect('/tasks/my-submissions/')


class MySubmissionListView(LoginRequiredMixin, View):
  def get( self, request ):
    if request.user.role != 'student':
      return redirect('/')
    submissions = Submission.objects.filter(student=request.user.student)
    return render(request, 'tasks/my_submissions.html', {
      'submissions': submissions
      }
                  )


class SubmissionsListTeacherView(LoginRequiredMixin, View):
  def get( self, request, assignment_id ):
    if request.user.role != 'teacher':
      return redirect('/')

    assignment = get_object_or_404(Assignment, assignment_id, teacher=request.user.teacher)
    submissions = Submission.objects.filter(assigment=assignment)
    return render(request, 'tasks/submission_list_teacher.html', {
      'assignment': assignment,
      'submissions': submissions
      }
                  )


class SubmissionCheckView(LoginRequiredMixin, View):
  def post( self, request, submission_id ):
    if request.user.role != 'teacher':
      return redirect('/')
    submission = get_object_or_404(Submission, id=submission_id, assignment__teacher=request.user.teacher)
    submission.grade = request.POST.get('grade')
    submission.checked = True
    submission.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))


class AssigmentDeleteView(LoginRequiredMixin, View):
  def post( self, request, assignment_id ):
    if request.user.role != 'teacher':
      return redirect('/')
    assignment = get_object_or_404(Assignment, id=assignment_id, teacher=request.user.teacher)
    assignment.delete()
    return redirect('/tasks/assignments/')