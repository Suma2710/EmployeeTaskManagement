from django import forms
from django.forms import ModelForm
from .models import MyUser, Task, EmployeeProfile
from django.core.validators import RegexValidator
from django.utils import timezone

class MyUserForm(ModelForm):
    phone_validator = RegexValidator(
        regex=r'^\d{10}$',
        message='Phone number must be exactly 10 digits.'
    )
    phn_no = forms.CharField(
        validators=[phone_validator],
        widget=forms.TextInput(attrs={'placeholder':'Enter Phone Number'})
    )
    class Meta:
        model = MyUser
        fields = ['username','password','email','phn_no','role','profile_image']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder':'Enter Your Name'}),
            'password': forms.PasswordInput(attrs={'placeholder':'Enter Password'}),
            'email': forms.EmailInput(attrs={'placeholder':'Enter Email'}),
        }

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=245)
    password = forms.CharField(widget=forms.PasswordInput)

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','assigned_to','complete_within']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':'Task Title'}),
            'description': forms.Textarea(attrs={'placeholder':'Task Description'}),
            'complete_within': forms.DateTimeInput(attrs={'type': 'datetime-local','min': timezone.now().strftime('%Y-%m-%dT%H:%M')}),
        }

class EmployeeProfileForm(ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ['employee','designation']
        widgets = {
            'designation': forms.TextInput(attrs={'placeholder':'Employee Designation'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].queryset = MyUser.objects.filter(role='employee',employee_profile__isnull=True)