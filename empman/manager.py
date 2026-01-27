from django.contrib.auth.base_user import BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(self,email,username='',phn_no=0,password=None,**extra_field):
        if not email:
            raise ValueError('Email is Important')
        user = self.model(email=self.normalize_email(email), **extra_field)
        user.username = username
        user.phn_no = phn_no
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username='',phn_no=0,password=None,**extra_field):
        extra_field.setdefault('is_superuser',True)
        extra_field.setdefault('is_staff',True)
        user = self.create_user(email=email,username=username,phn_no=phn_no,password=password,**extra_field)
        return user

    def create_manager(self,email,username='',phn_no=0,password=None,**extra_field):
        extra_field.setdefault('is_staff',True)
        extra_field.setdefault('is_manager',True)
        user = self.create_user(email=email,username=username,phn_no=phn_no,password=password,**extra_field)
        return user

    def create_employee(self,email,username='',phn_no=0,password=None,**extra_field):
        extra_field.setdefault('is_staff',False)
        extra_field.setdefault('is_employee',True)
        user = self.create_user(email=email,username=username,phn_no=phn_no,password=password,**extra_field)
        return user
