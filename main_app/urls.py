from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("auth/signup/", views.SignUpView.as_view(), name="signup"),
    path('tracker/add-student/', views.AddStudentView.as_view(), name='add_student'),
    path('tracker/students-list/', views.ListStudentsView.as_view(), name='students_list'), 
    path('tracker/student/<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('tracker/student/<int:pk>/edit/', views.UpdateStudentView.as_view(), name='edit_student'),
    path('tracker/<int:pk>/delete/', views.DeleteStudentView.as_view(), name='delete_student'),
    path('student/dashboard/', views.StudentDashboardView.as_view(), name='student_dashboard'),
]
