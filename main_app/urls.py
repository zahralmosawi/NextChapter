from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [
    path("auth/login/", views.CustomLoginView.as_view(), name="login"),

    path('tracker/add-student/', views.AddStudentView.as_view(), name='add_student'),
    path('tracker/students-list/', views.ListStudentsView.as_view(), name='students_list'), 
    path('tracker/student/<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('tracker/student/<int:pk>/edit/', views.UpdateStudentView.as_view(), name='edit_student'),
    path('tracker/<int:pk>/delete/', views.DeleteStudentView.as_view(), name='delete_student'),
    path('tracker/student/<int:student_id>/progress-log/create/', views.AddProgressLogView.as_view(), name='add_progress_log'),
    path('tracker/student/<int:pk>/progress-log/view/', views.ProgressLogDetailView.as_view(), name='progress_log_detail'),
    path('tracker/progress-log/<int:pk>/edit/', views.UpdateProgressLogView.as_view(), name='edit_progress_log'),
    path('tracker/student/<int:student_id>/log/<int:month_number>/', views.ListProgressLogsView.as_view(), name='monthly_logs'),

    path('events/add/', views.EventCreateView.as_view(), name='add_event'),

    path('student/dashboard/', views.StudentDashboardView.as_view(), name='student_dashboard'),
    path('student/change-password/', views.ChangePasswordView.as_view(), name='change_password'),
]