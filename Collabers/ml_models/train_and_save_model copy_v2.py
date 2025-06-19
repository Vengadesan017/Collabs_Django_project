import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
import random

# Load data
df = pd.read_csv('influencer_data.csv')

# Simulate brand_niche column using your Django NICHE_CHOICES
NICHE_CHOICES = [
    'food', 'it', 'fashion', 'travel', 'fitness', 'beauty', 'lifestyle', 'education',
    'finance', 'gaming', 'sports', 'automotive', 'home_decor', 'pets', 'entertainment',
    'eco', 'parenting', 'real_estate', 'books', 'luxury',
]

# Randomly assign brand niches for training/testing purposes
df['brand_niche'] = [random.choice(NICHE_CHOICES) for _ in range(len(df))]

# One-hot encode categorical variables: influencer 'category' and 'brand_niche'
df_encoded = pd.get_dummies(df, columns=['category', 'brand_niche'], drop_first=True)

# Define features and target
X = df_encoded.drop(columns=['Influencer_name', 'efficiency_prob'])  # drop name and target
y = df_encoded['efficiency_prob']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train XGBoost Regressor
model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, max_depth=4, learning_rate=0.1)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
rmse = mean_squared_error(y_test, y_pred)
print(f"Test RMSE: {rmse:.4f}")

# Save model
joblib.dump(model, 'xgboost_model_with_niches.pkl')
print("Model saved as 'xgboost_model_with_niches.pkl'")
