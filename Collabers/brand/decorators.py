from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps

def is_brand(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            if hasattr(request.user, 'account') and request.user.account.user_type == 'brand':
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "Access denied. Brand account required.")
                return redirect('auth:login')
        except Exception as e:
            messages.error(request, f"Something went wrong. Please try again:{e}")
            return redirect('auth:login')
    return wrapper
