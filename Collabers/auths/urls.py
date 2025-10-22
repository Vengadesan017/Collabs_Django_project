from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup', views.signup_view, name='signup'),
    path('verify', views.verify_otp_view, name='verify_otp'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('id/', views.get_id, name='getId'),
]
