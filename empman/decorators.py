from django.http import HttpResponse
from django.shortcuts import redirect
from functools import wraps

def role_base(required_role=None):
    """
    Decorator to restrict access to views based on user role.
    Usage:
        @role_base('manager')
        def manager_home(request):
            ...
    """
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                return redirect('login')
            if required_role == user.role:
                return func(request, *args, **kwargs)
            else:
                return HttpResponse(
                    '<div style="color:red; font-weight:bold;">You are not authorized for this page. Go back.</div>'
                )
        return inner
    return decorator
