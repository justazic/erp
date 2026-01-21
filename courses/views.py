from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Course, Group, Comment, Category


class CourseListView(View):
  def get( self, request ):
    courses = Course.objects.prefetch_related("sessions", "category")
    categories = Category.objects.all()

    return render(request, "courses/course_list.html", {
      "courses": courses,
      "categories": categories,
      },
                  )


class CourseDetailCreateView(View):
    def get(self, request):
        if request.user.role != 'admin':
            return redirect('/')
        return render(request, 'courses/course_create.html')

    @login_required
    def post(self, request):
        if request.user.role != 'admin':
            return redirect('/')

        Course.objects.create(
            name=request.POST.get('name')
        )
        return redirect('/courses/')





class GroupCreateView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role != 'admin':
            return redirect('/')

        courses = Course.objects.all()
        from accounts.models import User
        teachers = User.objects.filter(role='teacher')

        return render(
            request,
            'courses/group_create.html',
            {
                'courses': courses,
                'teachers': teachers
            }
        )

    def post(self, request):
        if request.user.role != 'admin':
            return redirect('/')

        Group.objects.create(
            name=request.POST.get('name'),
            course_id=request.POST.get('course'),
            teacher_id=request.POST.get('teacher')
        )
        return redirect('/courses/groups/')


class GroupListView(LoginRequiredMixin, View):
    def get(self, request):
        groups = Group.objects.select_related('course', 'teacher')
        return render(
            request,
            'courses/group_list.html',
            {'groups': groups}
        )


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request):
        Comment.objects.create(
            user=request.user,
            text=request.POST.get('text')
        )
        return redirect(request.META.get('HTTP_REFERER', '/'))

