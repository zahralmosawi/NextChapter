from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

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
    tracker_name = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': User.Role.TRACKER})
    comment = models.TextField(blank=True, null=True)

    class Meta: 
        db_table = 'progress_log'

    @property
    def month_number(self):
        from dateutil.relativedelta import relativedelta

        start_date = self.student.support_start_date
        log_date = self.date

        diff = relativedelta(log_date, start_date)
        months_diff = diff.years * 12 + diff.months # full months only ignore days

        # starting month is month 1
        return months_diff + 1 if months_diff >= 0 else 0 
    
    def __str__(self):
        return self.student.name + " - " + str(self.date)

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': User.Role.TRACKER})
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date']
    
    def __str__(self):
        return self.title
    
    def is_upcoming(self):
        return self.date >= timezone.now()