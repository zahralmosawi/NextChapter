from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        TRACKER = "tracker", "Tracker"
        STUDENT = "student", "Student"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)

# Student Profile
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    linkedin_url = models.CharField(max_length=255)
    cv_file = models.CharField(max_length=255)
    support_start_date = models.DateField()
    support_end_date = models.DateField()
    employment_status = models.CharField(max_length=20, choices=[('NOT_EMPLOYED', 'Not Employed'), ('EMPLOYED', 'Employed')], default='NOT_EMPLOYED')
    job_title = models.CharField(max_length=255, blank=True, null=True)
    job_start_date = models.DateTimeField(blank=True, null=True)

    class Meta: 
        db_table = 'student_profile'

    def __str__(self):
        return self.name

# Progress Log 
class ProgressLog(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    date = models.DateField()
    interaction_type = models.CharField(max_length=20, choices=[('CALL', 'Call'),('INTERVIEW', 'Interview'),('CV_UPDATE', 'CV Update'),('OTHER', 'Other')])
    status = models.CharField(max_length=20, choices=[('ANSWERED', 'Answered'), ('MISSED', 'Missed'),('COMPLETED', 'Completed'), ('PENDING', 'Pending')], default='PENDING')
    instructor_name = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta: 
        db_table = 'progress_log'

    def __str__(self):
        return self.student