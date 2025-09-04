from django import forms
from .models import User, StudentProfile, ProgressLog
from dateutil.relativedelta import relativedelta 

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user

class StudentProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = StudentProfile
        fields = ['name', 'email', 'linkedin_url', 'cv_file', 'support_start_date']

class ProgressLogForm(forms.ModelForm):
    class Meta:
        model = ProgressLog
        fields = ['date', 'interaction_type', 'status', 'instructor_name', 'comment']
