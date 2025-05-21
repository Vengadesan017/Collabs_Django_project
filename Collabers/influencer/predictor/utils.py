import joblib
import numpy as np

# Load model once
xgb_model = joblib.load('ml_models/xgboost_model.pkl')

def predict_efficiency(influencer):
    features = [
        influencer.channel_follower or 0,
        float(influencer.channel_engagement_rate or 0),
        influencer.channel_avg_like or 0,
        influencer.channel_avg_comments or 0
    ]
    prediction = xgb_model.predict(np.array(features).reshape(1, -1))
    return float(prediction[0])
