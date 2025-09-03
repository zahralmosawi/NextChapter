from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import View, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth import login
from .forms import SignUpForm, StudentProfileForm
from .models import User, StudentProfile

def is_tracker(user):
    return user.role == user.Role.TRACKER
def is_student(user):
    return user.role == user.Role.STUDENT


def home(request):
    return render(request, 'home.html')

class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'registration/sign-up.html', {'form': form})
    
    def post(self, request):
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('login')
        
        return render(request, 'registration/sign-up.html', {'form': form})
    

from django.conf import settings
import secrets    
from dateutil.relativedelta import relativedelta

class AddStudentView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = StudentProfile
    form_class = StudentProfileForm
    template_name = 'tracker/add_student.html'
    success_url = reverse_lazy('home')

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
    
class UpdateStudentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = StudentProfile
    form_class = StudentProfileForm
    template_name = 'tracker/add_student.html'

    def get_success_url(self):
        return reverse_lazy('student_detail', kwargs={'pk': self.object.pk})
    
    def test_func(self):
        return self.request.user.role == User.Role.TRACKER
