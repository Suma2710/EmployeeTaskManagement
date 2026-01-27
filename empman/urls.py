from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
      
    path('manager_home/', views.manager_home, name='manager_home'),
    path('employee_home/', views.employee_home, name='employee_home'),

    path('add_employee/', views.add_employee, name='add_employee'),
    path('assign_task/', views.assign_task, name='assign_task'),
    path('complete_task/<int:task_id>/', views.complete_task, name='complete_task'),
    path('delete_employee/<int:emp_id>/', views.delete_employee, name='delete_employee'),

    path('logout/', views.logout_view, name='logout'),
]
