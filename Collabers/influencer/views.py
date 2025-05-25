
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from brand.models import Post
from .models import Influencer, Applicant
from .forms import ApplicantForm
from auths.models import Account
from django.db.models import Q

# Create your views here.
from .predictor.utils import predict_efficiency
def create_applicant_with_prediction(influencer, post):
    prediction = predict_efficiency(influencer)
    
    applicant = Applicant.objects.create(
        influencer=influencer,
        post=post,
        efficiency_prob=prediction
    )
    print("==========")
    print(applicant)
    print("==========")
    return applicant

# Utility to get influencer based on user
def get_influencer(request):
    account = Account.objects.get(user=request.user)
    return get_object_or_404(Influencer, influ_acc=account)

@login_required
def Collabs_view(request):
    influencer = get_influencer(request)
    if request.method == 'POST':
        try:
            account = Account.objects.get(user=request.user)
            influencer = Influencer.objects.get(influ_acc=account)
            post_id = request.POST.get('id')
            post = get_object_or_404(Post, post_id=post_id)

            # Prevent duplicate application
            existing = Applicant.objects.filter(post=post, influencer=influencer).exists()
            if existing:
                messages.warning(request, "You have already applied to this post.")
            else:
                # Applicant.objects.create(post=post, influencer=influencer)
                create_applicant_with_prediction(influencer,post)
                messages.success(request, "Application submitted successfully.")
        except Exception as e:
            messages.error(request, f"Failed to apply: {e}")
        return redirect('influencer:applied', filter='sds')
    else:
        applied_post_ids = Applicant.objects.filter(influencer=influencer).values_list('post_id', flat=True)
        
        available_posts = Post.objects.filter(
            is_open=True
        ).exclude(post_id__in=applied_post_ids).order_by('-post_id')

        return render(request, 'influencer/collabs.html', {'posts': available_posts})


@login_required
def Applied_view(request, filter):
    influencer = get_influencer(request)
    
    # Handle form submissions
    print("----------------")
    if request.method == 'POST':
        try :
            print("📥 POST request received.")
            appli_id = request.POST.get('id')
            print(f"➡️ Application ID: {appli_id}")

            applicant = get_object_or_404(Applicant, pk=appli_id, influencer=influencer)
            print(f"📄 Applicant found: {applicant}")

            if 'run_again' in request.POST:
                print("🔁 'Run again' button clicked.")
                applicant.is_stoped = False
                applicant.is_posted = True
                applicant.save()
                messages.success(request, "Ad has been reactivated.")
                print("✅ Ad reactivated.")

            elif 'stop' in request.POST:
                print("⛔ 'Stop' button clicked.")
                applicant.is_stoped = True
                applicant.save()
                messages.success(request, "Ad has been stopped.")
                print("✅ Ad stopped.")

            elif 'publish' in request.POST:
                print("🚀 'Publish' button clicked.")
                applicant.is_posted = True
                applicant.save()
                messages.success(request, "Ad has been published.")
                print("✅ Ad published.")

            elif 'work_completed' in request.POST:
                print("📤 'Work completed' button clicked.")
                url = request.POST.get('url')
                summary = request.POST.get('summary')
                ads_file = request.FILES.get('ads_file')

                print(f"🌐 URL: {url}")
                print(f"📝 Summary: {summary}")
                print(f"📁 File uploaded: {bool(ads_file)}")

                if not url or not summary:
                    messages.error(request, "URL and summary are required.")
                    print("❌ Missing URL or summary.")
                else:
                    applicant.is_worked = True
                    applicant.url = url
                    applicant.summary = summary
                    if ads_file:
                        applicant.ads_file = ads_file
                    applicant.save()
                    messages.success(request, "Work submitted for brand verification.")
                    print("✅ Work submitted.")

            else:
                print("⚠️ No recognized submit button found.")

            return redirect('influencer:applied', filter=filter)
        except Exception as e:
            messages.error(request, f"Failed to apply: {e}")

    # Filtering applicants
    applicants = Applicant.objects.filter(influencer=influencer)

    if filter == 'pending':
        applicants = applicants.filter(is_confirmed=False)
    elif filter == 'in-work':
        applicants = applicants.filter(is_confirmed=True,is_worked=False)
    elif filter == 'verification-wait':
        applicants = applicants.filter(is_worked=True,is_verified=False)
    elif filter == 'verified':
        applicants = applicants.filter(is_verified=True,is_posted=False)
    elif filter == 'running':
        applicants = applicants.filter(is_posted=True,is_stoped=False)
    elif filter == 'in-active':
        applicants = applicants.filter(is_stoped=True)

        

    return render(request, 'influencer/applied.html', {'applicants': applicants, 'filter': filter})


@login_required
def Payment_view(request):
    influencer = get_influencer(request)
    paid_apps = Applicant.objects.filter(influencer=influencer, is_payed=True)
    unpaid_apps = Applicant.objects.filter(influencer=influencer, is_payed=False)

    return render(request, 'influencer/payment.html', {
        'paid': paid_apps,
        'unpaid': unpaid_apps
    })


@login_required
def Profile_view(request):
    influencer = get_influencer(request)
    return render(request, 'influencer/profile.html', {'influencer': influencer})