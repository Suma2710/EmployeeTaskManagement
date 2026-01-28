from django.shortcuts import render, redirect
from .forms import MyUserForm, LoginForm, TaskForm, EmployeeProfileForm
from .models import MyUser, Task, EmployeeProfile
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .decorators import role_base
from django.http import HttpResponse
from django.utils import timezone

def signup(request):
    if request.method == 'POST':
        userform = MyUserForm(request.POST, request.FILES)
        if userform.is_valid():
            name = userform.cleaned_data['username']
            email = userform.cleaned_data['email']
            phn_no = userform.cleaned_data['phn_no']
            password = userform.cleaned_data['password']
            role = userform.cleaned_data['role']
            profile_image = userform.cleaned_data['profile_image']
            if role == 'employee':
                user = MyUser.objects.create_user(email,username=name,phn_no=phn_no,password=password,role=role)
            elif role == 'manager':
                user = MyUser.objects.create_manager(email,username=name,phn_no=phn_no,password=password,role=role)

            if profile_image:
                user.profile_image = profile_image
                user.save()
            return redirect('login')
        else:
            return render(request, 'signup.html', {'userform': userform})
    else:
        userform = MyUserForm()
    return render(request,'signup.html',{'userform':userform})

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(email=login_form.cleaned_data['email'], password=login_form.cleaned_data['password'])
            if user is not None:
                auth_login(request,user)
                if user.role == 'manager':
                    return redirect('manager_home')
                elif user.role == 'employee':
                    return redirect('employee_home')
            else:
                return render(request, 'login.html', {'login_form': login_form, 'error': 'Invalid email or password'})
                
    else:
        login_form = LoginForm()
    return render(request,'login.html',{'login_form':login_form})

@role_base('manager')
def manager_home(request):
    employees = EmployeeProfile.objects.filter(manager=request.user)
    tasks = Task.objects.filter(assigned_by=request.user)
    return render(request,'manager_home.html',{'employees':employees,'tasks':tasks})

@role_base('employee')
def employee_home(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request,'employee_home.html',{'tasks':tasks})

@role_base('manager')
def assign_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_by = request.user
            task.status = 'pending'
            task.save()
            return redirect('manager_home')
        else:
            return render(request, 'assign_task.html', {'form': form})
    else:
        form = TaskForm()
        form.fields['assigned_to'].queryset = MyUser.objects.filter(employee_profile__manager=request.user)
    return render(request,'assign_task.html',{'form':form})


@role_base('employee')
def complete_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id, assigned_to=request.user)
        task.status = 'done'
        task.completed_at = timezone.now()
        task.save()
        return redirect('employee_home')
    except Task.DoesNotExist:
        return HttpResponse('Task not found or not assigned to you')


@role_base('manager')
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeProfileForm(request.POST, request.FILES)
        if form.is_valid():
            employee_profile = form.save(commit=False)
            employee_profile.manager = request.user
            employee_profile.save()
            return redirect('manager_home')
    else:
        form = EmployeeProfileForm()

    return render(request, 'add_employee.html', {'form': form})

@role_base('manager')
def delete_employee(request, emp_id):
    try:
        emp_profile = EmployeeProfile.objects.get(id=emp_id, manager=request.user)
        emp_profile.employee.delete()  
        emp_profile.delete()           
        return redirect('manager_home')
    except EmployeeProfile.DoesNotExist:
        return HttpResponse('Employee not found')

def logout_view(request):
    auth_logout(request)
    return redirect('login')