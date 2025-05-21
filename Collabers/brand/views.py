from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.db.models import Prefetch, Count

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PostForm, ApplicantForm, BrandProfileForm
from .models import Post, Brand
from auths.models import Account
from influencer.models import Applicant
from .decorators import is_brand




@login_required
@is_brand
def Post_view(request):
    try:
        account = Account.objects.get(user=request.user)
        posts = Post.objects.filter(brand__brand_acc=account).order_by('-post_id')
        return render(request, 'brand/posts.html', {'posts': posts})
    except Exception as e:
        messages.error(request, f"Failed to load posts: {e}")
        return render(request, 'brand/posts.html', {'posts': []})
    
    
@login_required
@is_brand
def NewPost_view(request):
    try:
        account = Account.objects.get(user=request.user)
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.brand = Brand.objects.get(brand_acc=account)
                post.save()
                messages.success(request, "Post created successfully.")
                return redirect('brand:post')
            else:
                messages.error(request, "Invalid form submission.")
        else:
            form = PostForm()
        return render(request, 'brand/new_post.html', {'form': form})
    except Exception as e:
        messages.error(request, f"Something went wrong:{e}")
        return redirect('brand:post')
    
    
@login_required
@is_brand
def FilterPost_view(request, filter):
    try:
        account = Account.objects.get(user=request.user)
        if filter == "active":
            posts = Post.objects.filter(is_open=True, brand__brand_acc=account).order_by('-post_id')
        elif filter == "in-active":
            posts = Post.objects.filter(is_open=False, brand__brand_acc=account).order_by('-post_id')
        return render(request, 'brand/posts.html', {'posts': posts, 'filter': filter})
    except Exception:
        messages.error(request, f"Error filtering posts:{e}")
        return redirect('brand:post')

@login_required
@is_brand
def Applicants_view(request):
    account = Account.objects.get(user=request.user)
    # posts = Post.objects.filter(brand__brand_acc=account).order_by('-post_id')
    # posts = Post.objects.annotate(
    #         is_applied=Exists(job_application_exists),
    #         is_saved=Exists(bookmarks_exists)
    #         ).filter(brand__brand_acc=account).order_by('-post_id')
    posts = Post.objects.filter(
        brand__brand_acc=account
    ).annotate(
        applicant_count=Count('applicant_post')  # Related name in Applicant
    ).order_by('-applicant_count', '-post_id')
    applicants = Applicant.objects.all()
    return render(request, 'brand/applicants.html', {'posts': posts})

@login_required
@is_brand
def ApplicantsFilter_view(request,appli_id):
    account = Account.objects.get(user=request.user)
    applicants = Applicant.objects.filter(post=appli_id).order_by('-efficiency_prob')
    print(applicants)
    return render(request, 'brand/filter_applicants.html', {'applicants': applicants})

@login_required
@is_brand
def Verification_view(request):
    account = Account.objects.get(user=request.user)
    verified_applicants = Applicant.objects.filter(is_verified=True)
    return render(request, 'brand/verification.html', {'verified_applicants': verified_applicants})

@login_required
@is_brand
def Profile_view(request):
    account = Account.objects.get(user=request.user)
    # Assuming you have a way to get the current brand, e.g., via request.user
    brand = get_object_or_404(Brand, brand_acc=account  )
    return render(request, 'brand/profile.html', {'brand': brand})