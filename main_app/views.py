from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import View, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth import login
from .forms import SignUpForm
from .models import User, StudentProfile, ProgressLog

def is_tracker(u):
    return u.role == u.Role.TRACKER

def is_student(u):
    return u.role == u.Role.STUDENT

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