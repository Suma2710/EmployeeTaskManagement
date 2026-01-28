from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid
from .manager import MyUserManager
from django.utils import timezone

class MyUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    username = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, unique=True)
    phn_no = models.PositiveBigIntegerField(unique=True)
    acc_created_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=10,choices=[('manager','MANAGER'),('employee','EMPLOYEE')])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_manager = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='empman_users',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='empman_users_permissions',
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','phn_no']

    objects = MyUserManager()

    def __str__(self):
        return f"{self.username} ({self.role})"


# Employee profile linked to manager
class EmployeeProfile(models.Model):
    employee = models.OneToOneField(
        MyUser,
        on_delete=models.CASCADE,
        related_name='employee_profile'
    )
    manager = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='employees'
    )
    designation = models.CharField(max_length=100, blank=True)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.username}, Manager: {self.manager.username}"


# Task model
class Task(models.Model):
    STATUS_CHOICES = (
        ('pending','Pending'),
        ('done','Done'),
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_by = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='tasks_created'
    )
    assigned_to = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='tasks_received'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    complete_within = models.DateTimeField(blank=True, null=True)
    overdue = models.BooleanField(default=False)
    completed_within = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}, {self.assigned_to.username}"



