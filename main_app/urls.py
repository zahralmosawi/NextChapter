from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("auth/signup/", views.SignUpView.as_view(), name="signup"),
    path('tracker/add-student/', views.AddStudentView.as_view(), name='add_student'),
    path('tracker/students-list/', views.ListStudentsView.as_view(), name='students_list'), 
]
