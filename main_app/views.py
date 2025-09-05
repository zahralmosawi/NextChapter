from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import View, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth import login
from .forms import StudentProfileForm, ProgressLogForm
from .models import User, StudentProfile, ProgressLog

def is_tracker(user):
    return user.role == user.Role.TRACKER
def is_student(user):
    return user.role == user.Role.STUDENT


def home(request):
    return render(request, 'home.html')

from django.conf import settings
import secrets    
from dateutil.relativedelta import relativedelta

class AddStudentView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = StudentProfile
    form_class = StudentProfileForm
    template_name = 'tracker/add_student.html'
    success_url = reverse_lazy('students_list')

    def test_func(self):
        return self.request.user.role == User.Role.TRACKER

    def form_valid(self, form):
        temp_password = secrets.token_urlsafe(8)
        student_email = form.cleaned_data.get('email')

        student_user = User.objects.create_user(
            username=student_email,
            email=student_email,
            password=temp_password,
            role=User.Role.STUDENT
        )

        student_profile = form.save(commit=False)
        student_profile.user = student_user

        student_profile.support_end_date = student_profile.support_start_date + relativedelta(months=+9)
        student_profile.save()

        
        print(f"STUDENT ACCOUNT CREATED!!!")
        print(f"Email: {student_email}")
        print(f"Temp Password: {temp_password}")

        return redirect(self.success_url)
    
class ListStudentsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = StudentProfile
    template_name = 'tracker/students_list.html'
    context_object_name = 'students'

    def test_func(self):
        return self.request.user.role == User.Role.TRACKER

class StudentDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = StudentProfile
    template_name = 'tracker/student_detail.html'
    context_object_name = 'student'

    def test_func(self):
        return self.request.user.role == User.Role.TRACKER
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.get_object()
        progress_logs = ProgressLog.objects.filter(student=student).order_by('-date')
        context['progress_logs'] = progress_logs
        return context
    
class UpdateStudentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = StudentProfile
    form_class = StudentProfileForm
    template_name = 'tracker/add_student.html'

    def get_success_url(self):
        return reverse_lazy('student_detail', kwargs={'pk': self.object.pk})
    
    def test_func(self):
        return self.request.user.role == User.Role.TRACKER
    
class DeleteStudentView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = StudentProfile
    success_url = reverse_lazy('students_list')

    def test_func(self):
        return self.request.user.role == User.Role.TRACKER
    
class AddProgressLogView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ProgressLog
    form_class = ProgressLogForm
    template_name = 'tracker/add_progress_log.html'

    def test_func(self):
        return self.request.user.role == User.Role.TRACKER
    
    def has_max_logs(self, student):
        existing_months = set()
        for log in ProgressLog.objects.filter(student=student):
            existing_months.add(log.month_number)
        return len(existing_months) >= 9
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.kwargs['student_id']
        student = StudentProfile.objects.get(id=student_id)
        context['student'] = student
        context['max_logs_reached'] = self.has_max_logs(student)
        return context
    
    def form_valid(self, form):
        student_id = self.kwargs['student_id']
        student = StudentProfile.objects.get(id=student_id)

        if self.has_max_logs(student):
            form.add_error(None, "Maximum of 9 monthly logs already reached! Cannot add more logs")
            return self.form_invalid(form)
        
        form.instance.student = student
        form.instance.tracker_name = self.request.user 
        return super().form_valid(form)
    
    def get_success_url(self):
        student_id = self.kwargs['student_id']
        return reverse_lazy('student_detail', kwargs={'pk': student_id})

class ListProgressLogsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ProgressLog
    template_name = 'tracker/monthly_logs_list.html'
    context_object_name = 'progress_logs'

    def test_func(self):
        return self.request.user.role == User.Role.TRACKER
    
    def get_queryset(self):
        student_id = self.kwargs['student_id']
        month_number = self.kwargs['month_number']
        logs = ProgressLog.objects.filter(student_id=student_id)
        return [log for log in logs if log.month_number == month_number]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.kwargs['student_id']
        month_number = self.kwargs['month_number']
        
        context['student'] = StudentProfile.objects.get(id=student_id)
        context['month_number'] = month_number
        context['total_months'] = 9  
        
        return context

class ProgressLogDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = ProgressLog
    template_name = 'tracker/progress_log_detail.html'
    context_object_name = 'progress_log'

    def test_func(self):
        return self.request.user.role == User.Role.TRACKER
    
class UpdateProgressLogView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ProgressLog
    form_class = ProgressLogForm
    template_name = 'tracker/add_progress_log.html'

    def test_func(self):
        return self.request.user.role == User.Role.TRACKER
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = self.object.student
        return context
    
    def get_success_url(self):
        return reverse_lazy('progress_log_detail', kwargs={'pk': self.object.pk})
    
# Student Views
class StudentDashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'student/dashboard.html'
    context_object_name = 'student'

    def test_func(self):
        return self.request.user.role == User.Role.STUDENT

    def get(self, request):
        student_profile = StudentProfile.objects.get(user=request.user)
        print(f"StudentProfile found: {student_profile} for user {request.user} (id={request.user.id})")
        # progress_logs = ProgressLog.objects.filter(student=student_profile).order_by('-date')
        return render(request, 'student/dashboard.html', {'student': student_profile})