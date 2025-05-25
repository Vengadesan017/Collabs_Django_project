from django.urls import path
from . import views

app_name = 'brand'

urlpatterns = [
    path('', views.Post_view, name='post'),
    path('new-post/',views.NewPost_view, name="new_post"),
    path('filter-post/<str:filter>',views.FilterPost_view, name="filter_post"),
    path('applicants/',views.Applicants_view,name="applicants"),
    path('filter-applicants/<int:post_id>',views.ApplicantsFilter_view,name="filter_applicants"),
    path('verification/<str:filter>',views.Verification_view,name='verification'),
    path('profile',views.Profile_view,name='profile'),
]
