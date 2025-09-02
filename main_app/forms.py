from django import forms
from .models import User, StudentProfile
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
    class Meta:
        model = StudentProfile
        fields = ['name', 'linkedin_url', 'cv_file', 'support_start_date']

        def save(self, commit=True):
            profile = super().save(commit=False)

            start_date = profile.support_start_date
            profile.end_date = start_date + relativedelta(months=+9)

            if commit:
                profile.save()

            return profile
