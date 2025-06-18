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


def home_view(request):
    return render(request,'auth/index.html')



def get_id(request):
    name = False
    if request.method == 'POST':
        name = request.POST['name']
        id = get_channel_id_from_handle(name)
        fetch_and_store_channel_data_print(id)
        
    return render(request,'auth/id.html',{'id':id})



# Get data from APi 

def get_channel_id_from_handle(handle):
    if handle.startswith("@"):
        handle = handle[1:]  # remove @

    url = f"https://www.googleapis.com/youtube/v3/channels?part=id&forHandle={handle}&key={settings.YOUTUBE_API_KEY}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "items" in data and len(data["items"]) > 0:
            return data["items"][0]["id"]
        else:
            print(f"No channel found for handle: @{handle}")
            return None

    except Exception as e:
        print(f"[ERROR] Could not get channel ID from handle: {e}")
        return None





#  Auto fetch
import requests
from django.conf import settings
from influencer.models import Influencer
from datetime import datetime

def fetch_and_store_channel_data(channel_id, influencer=None):
    """
    Fetch YouTube channel data and update the Influencer instance.
    """
    url = (
        "https://www.googleapis.com/youtube/v3/channels"
        f"?part=snippet,statistics&id={channel_id}&key={settings.YOUTUBE_API_KEY}"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "items" not in data or not data["items"]:
            print(f"No data found for channel ID: {channel_id}")
            return

        info = data["items"][0]
        snippet = info.get("snippet", {})
        stats = info.get("statistics", {})
        # print(data)
        # Safely parse and update
        influencer.channel_name = snippet.get("title", influencer.channel_name)
        influencer.channel_id = channel_id
        influencer.channel_description = snippet.get("description", "")

        published_at = snippet.get("publishedAt")
        if published_at:
            influencer.channel_created_at = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")

        influencer.channel_thumbnail_url = (
            snippet.get("thumbnails", {}).get("default", {}).get("url", "")
        )

        influencer.channel_follower = int(stats.get("subscriberCount", 0))
        influencer.channel_total_views = int(stats.get("viewCount", 0))
        influencer.channel_video_count = int(stats.get("videoCount", 0))

        influencer.save()

        print(f"YouTube channel data stored for: {channel_id}")

    except requests.RequestException as e:
        print(f"[ERROR] YouTube API fetch failed: {e}")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")












def fetch_and_store_channel_data_print(channel_id, influencer=None):
    """
    Fetch YouTube channel data and update the Influencer instance.
    """
    url = (
        "https://www.googleapis.com/youtube/v3/channels"
        f"?part=snippet,statistics&id={channel_id}&key={settings.YOUTUBE_API_KEY}"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "items" not in data or not data["items"]:
            print(f"No data found for channel ID: {channel_id}")
            return

        info = data["items"][0]
        snippet = info.get("snippet", {})
        stats = info.get("statistics", {})
        print(data)
        # # Safely parse and update
        # influencer.channel_name = snippet.get("title", influencer.channel_name)
        # influencer.channel_id = channel_id
        # influencer.channel_description = snippet.get("description", "")

        # published_at = snippet.get("publishedAt")
        # if published_at:
        #     influencer.channel_created_at = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")

        # influencer.channel_thumbnail_url = (
        #     snippet.get("thumbnails", {}).get("default", {}).get("url", "")
        # )

        # influencer.channel_follower = int(stats.get("subscriberCount", 0))
        # influencer.channel_total_views = int(stats.get("viewCount", 0))
        # influencer.channel_video_count = int(stats.get("videoCount", 0))

        # influencer.save()

        print(f"YouTube channel data stored for: {channel_id}")

    except requests.RequestException as e:
        print(f"[ERROR] YouTube API fetch failed: {e}")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
