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
        posts = Post.objects.filter(
            brand__brand_acc=account
        ).annotate(
            applicant_count=Count('applicant_post')  # Related name in Applicant
        ).order_by('-applicant_count', '-post_id')
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
def FilterPost_view(request, filter=None):
    try:
        account = Account.objects.get(user=request.user)
        if filter == "active":
            posts = Post.objects.filter(
                brand__brand_acc=account,
                is_open=True
            ).annotate(
                applicant_count=Count('applicant_post')  # Related name in Applicant
            ).order_by('-applicant_count', '-post_id')
        elif filter == "in-active":
            posts = Post.objects.filter(
                brand__brand_acc=account,
                is_open=False
            ).annotate(
                applicant_count=Count('applicant_post')  # Related name in Applicant
            ).order_by('-applicant_count', '-post_id')
        else:
            posts = Post.objects.filter(
                brand__brand_acc=account
            ).annotate(
                applicant_count=Count('applicant_post')  # Related name in Applicant
            ).order_by('-applicant_count', '-post_id')
            # posts = Post.objects.filter(is_open=False, brand__brand_acc=account).order_by('-post_id')
        return render(request, 'brand/posts.html', {'posts': posts, 'filter': filter})
    except Exception:
        messages.error(request, f"Error filtering posts:{Exception}")
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
def ApplicantsFilter_view(request,post_id):
    account = Account.objects.get(user=request.user)
    if request.method == 'POST':
        applicant = get_object_or_404(Applicant, appli_id=request.POST.get('id'))
        applicant.is_confirmed = True
        applicant.save()
        messages.success(request, "Applicant is confirmed successfully.")
        return redirect("brand:filter_applicants", post_id=post_id)
    applicants = Applicant.objects.filter(post=post_id).order_by('-efficiency_prob')
    return render(request, 'brand/filter_applicants.html', {'applicants': applicants})

@login_required
@is_brand
def Verification_view(request,filter):
    account = Account.objects.get(user=request.user)
    if request.method == 'POST':
        applicant = get_object_or_404(Applicant, appli_id=request.POST.get('id'))
        applicant.is_verified = True
        applicant.remarks = request.POST.get('remarks')
        applicant.save()
        messages.success(request, "Applicant is Verified successfully.")
        return redirect("brand:verification", filter='actioned')
    if filter == 'running':
        verified_applicants = Applicant.objects.filter(post__brand__brand_acc=account,is_confirmed=True,is_posted=True,is_stoped=False).order_by('-is_worked')
    elif filter == 'closed':
        verified_applicants = Applicant.objects.filter(post__brand__brand_acc=account,is_confirmed=True,is_stoped=True).order_by('-is_worked')
    elif filter == 'verified':
        verified_applicants = Applicant.objects.filter(post__brand__brand_acc=account,is_confirmed=True,is_posted=False,is_stoped=False,is_worked=True,is_verified=False).order_by('-is_worked')
    elif filter == 'complete':
        verified_applicants = Applicant.objects.filter(post__brand__brand_acc=account,is_confirmed=True,is_posted=False,is_stoped=False,is_worked=False,is_verified=False).order_by('-is_worked')
    elif filter == 'publish':
        verified_applicants = Applicant.objects.filter(post__brand__brand_acc=account,is_confirmed=True,is_posted=False,is_stoped=False,is_worked=True,is_verified=True).order_by('-is_worked')
    else:
        verified_applicants = Applicant.objects.filter(post__brand__brand_acc=account).order_by('-is_worked')
    return render(request, 'brand/verification.html', {'verified_applicants': verified_applicants})

@login_required
@is_brand
def Profile_view(request):
    account = Account.objects.get(user=request.user)
    # Assuming you have a way to get the current brand, e.g., via request.user
    brand = get_object_or_404(Brand, brand_acc=account  )
    return render(request, 'brand/profile.html', {'brand': brand})


@login_required
def Payment_view(request):
    account = Account.objects.get(user=request.user)
    paid_apps = Applicant.objects.filter(post__brand__brand_acc=account, is_payed=True).order_by('-is_posted','-amount')
    unpaid_apps = Applicant.objects.filter(post__brand__brand_acc=account, is_payed=False).order_by('-is_posted','-amount')
    brand = get_object_or_404(Brand, brand_acc=account  )
    return render(request, 'brand/payment.html', {
        'paid': paid_apps,
        'unpaid': unpaid_apps,
        'brand': brand
    })
