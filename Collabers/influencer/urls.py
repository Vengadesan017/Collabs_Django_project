from django.urls import path
from . import views

app_name = 'influencer'

urlpatterns = [
    path('', views.Collabs_view, name='collabs'),
    path('Applied/<str:filter>',views.Applied_view, name="applied"),
    path('Payment/',views.Payment_view, name="payment"),
    path('profile',views.Profile_view,name='profile'),
]
