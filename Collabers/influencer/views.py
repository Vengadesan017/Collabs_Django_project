from django.shortcuts import render

from .models import Applicant

# Create your views here.
from predictor.utils import predict_efficiency
def create_applicant_with_prediction(influencer, post):
    prediction = predict_efficiency(influencer)
    
    applicant = Applicant.objects.create(
        influencer=influencer,
        post=post,
        efficiency_prob=prediction
    )
    return applicant