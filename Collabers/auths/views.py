from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from brand.forms import BrandProfileForm
from auths.models import Account
from influencer.models import Influencer
from brand.models import Brand
from django.contrib import messages


import random
from decimal import Decimal

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create Account record for the user
            user_type = request.POST.get("role")
            acc = Account.objects.create(user=user, user_type=user_type)
            
            login(request, user)
            # Redirect to the appropriate page based on user type
            if user_type == 'brand':
                Brand.objects.create(
                    brand_acc=acc,
                    brand_name=request.POST.get("brand_name"),
                    brand_niche=request.POST.get("brand_niche")
                )
                return redirect('brand:post')  
            elif user_type == 'influencer':
                Influencer.objects.create(
                    influ_acc=acc,
                    channel_name=request.POST.get("influencer_channel_name"),
                    channel_id=request.POST.get("influencer_channel_id"),
                    channel_niche=request.POST.get("influencer_niche"),
                    channel_follower=random.randint(1000, 1000000),
                    channel_engagement_rate=Decimal(random.uniform(1.0, 15.0)).quantize(Decimal('0.0000000001')),
                    channel_avg_like=random.randint(50, 50000),
                    channel_avg_comments=random.randint(10, 5000)
                )
                return redirect('influencer:collabs')  
            elif user_type == 'admin':
                return redirect('admin') 
            else:
                return redirect('auth:login') 
            
        else:
            messages.error(request, form.errors)        
            redirect("auth:signup")
    else:
        form = SignUpForm()
    return render(request, 'auth/signup.html', {'form': form, 'brand':BrandProfileForm()})

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
            elif user_type == 'influencer':
                return redirect('influencer:collabs')  
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
