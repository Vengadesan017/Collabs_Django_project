from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from auths.models import Account
from django.contrib import messages

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create Account record for the user
            user_type = form.cleaned_data['user_type']
            Account.objects.create(user=user, user_type=user_type)
            
            login(request, user)
            # Redirect to the appropriate page based on user type
            if user_type == 'brand':
                return redirect('brand:post')  
            # elif user_type == 'influencer':
            #     return redirect('influencer:collab')  
            # elif user_type == 'admin':
            #     return redirect('admin:home') 
            else:
                return redirect('auth:login') 
            
        else:
            messages.error(request, form.errors)        
    else:
        form = SignUpForm()
    return render(request, 'auth/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            account = Account.objects.get(user=user)
            user_type = account.user_type
            
            login(request, user)
            # Redirect to the appropriate page based on user type
            if user_type == 'brand':
                return redirect('brand:post')  
            # elif user_type == 'influencer':
            #     return redirect('influencer:collab')  
            # elif user_type == 'admin':
            #     return redirect('admin:home') 
            else:
                return redirect('auth:signup') 
            
            return redirect('auth:signup')  # Replace with your app's homepage
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    return redirect('auth:login')  # Or your preferred redirect
