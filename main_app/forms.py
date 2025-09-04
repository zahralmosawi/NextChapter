from django import forms
from .models import User, StudentProfile, ProgressLog
from dateutil.relativedelta import relativedelta 

class StudentProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = StudentProfile
        fields = ['name', 'email', 'linkedin_url', 'cv_file', 'support_start_date']

class ProgressLogForm(forms.ModelForm):
    class Meta:
        model = ProgressLog
        fields = ['date', 'interaction_type', 'status', 'tracker_name', 'comment']
