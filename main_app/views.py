from django.shortcuts import render
from .models import User, StudentProfile, ProgressLog
from django.contrib.auth.decorators import login_required, user_passes_test

def is_tracker(u):
    return u.role == u.Role.TRACKER

def is_student(u):
    return u.role == u.Role.STUDENT

def home(request):
    return render(request, 'home.html')
