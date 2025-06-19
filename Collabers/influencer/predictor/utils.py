import joblib
import numpy as np
import pandas as pd

# Load the trained model
xgb_model = joblib.load('ml_models/xgboost_model_with_niches.pkl')

# Feature columns used during model training
FEATURE_COLUMNS = [
    'channel_follower', 'channel_engagement_rate', 'channel_avg_like', 'channel_avg_comments',
    'category_fitness', 'category_food', 'category_tech', 'category_travel',
    'brand_niche_beauty', 'brand_niche_books', 'brand_niche_eco', 'brand_niche_education',
    'brand_niche_entertainment', 'brand_niche_fashion', 'brand_niche_finance',
    'brand_niche_fitness', 'brand_niche_food', 'brand_niche_gaming', 'brand_niche_home_decor',
    'brand_niche_it', 'brand_niche_lifestyle', 'brand_niche_luxury', 'brand_niche_parenting',
    'brand_niche_pets', 'brand_niche_real_estate', 'brand_niche_sports', 'brand_niche_travel'
]

def predict_efficiency(influencer, post):
    # Extract niches
    brand_niche = post.brand.brand_niche
    influencer_niche = influencer.channel_niche

    # Core features
    data = {
        'channel_follower': influencer.channel_follower or 0,
        'channel_engagement_rate': float(influencer.channel_engagement_rate or 0),
        'channel_avg_like': influencer.channel_avg_like or 0,
        'channel_avg_comments': influencer.channel_avg_comments or 0,
    }

    # One-hot encode influencer category (only those used in training)
    for niche in ['fitness', 'food', 'tech', 'travel']:
        data[f'category_{niche}'] = int(influencer_niche == niche)

    # One-hot encode brand niche (only those used in training)
    for niche in [
        'beauty', 'books', 'eco', 'education', 'entertainment', 'fashion',
        'finance', 'fitness', 'food', 'gaming', 'home_decor', 'it',
        'lifestyle', 'luxury', 'parenting', 'pets', 'real_estate',
        'sports', 'travel'
    ]:
        data[f'brand_niche_{niche}'] = int(brand_niche == niche)

    # Build DataFrame
    df = pd.DataFrame([data])
    df = df.reindex(columns=FEATURE_COLUMNS, fill_value=0)

    # Predict
    prediction = xgb_model.predict(df)
    return float(prediction[0])
