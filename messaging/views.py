from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from courses.models import Group
from .forms import MessageForm
from students.models import Enrollment

class GroupChatListView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        if user.role == 'teacher':
            groups = Group.objects.filter(teacher=user).select_related('course')
        elif user.role == 'student':
            # Only show groups that the student is directly enrolled in
            groups = Group.objects.filter(enrollments__student=user).select_related('course').distinct()
        else:
            groups = Group.objects.all().select_related('course')
        
        return render(request, 'messaging/group_list.html', {'groups': groups})

class GroupChatDetailView(LoginRequiredMixin, View):
    def get(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        # Access check - only allow if student is enrolled in this specific group
        if request.user.role == 'student':
            is_enrolled = Enrollment.objects.filter(student=request.user, group=group).exists()
            if not is_enrolled:
                return redirect('messaging:group_list')
        elif request.user.role == 'teacher':
            if group.teacher != request.user:
                return redirect('messaging:group_list')

        messages = group.messages.all().select_related('sender')
        form = MessageForm()
        return render(request, 'messaging/chat.html', {
            'group': group,
            'messages': messages,
            'form': form
        })

    def post(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        # Access check - only allow if student is enrolled in this specific group
        if request.user.role == 'student':
            is_enrolled = Enrollment.objects.filter(student=request.user, group=group).exists()
            if not is_enrolled:
                return redirect('messaging:group_list')
        elif request.user.role == 'teacher':
            if group.teacher != request.user:
                return redirect('messaging:group_list')

        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.group = group
            message.sender = request.user
            message.save()
        return redirect('messaging:chat_detail', group_id=group.id)
