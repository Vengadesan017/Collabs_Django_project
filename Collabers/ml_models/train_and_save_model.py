import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

# Load your dataset
# Make sure to update the path to your actual CSV file
df = pd.read_csv('influencer_data.csv')

# Print columns to confirm
print("Columns:", df.columns)

# Example: Assuming your CSV has these columns (adjust as needed)
# ['channel_follower', 'channel_engagement_rate', 'channel_avg_like', 'channel_avg_comments', 'efficiency_prob']

# Define features (X) and target (y)
X = df[['channel_follower', 'channel_engagement_rate', 'channel_avg_like', 'channel_avg_comments']]
y = df['efficiency_prob']

# Train-test split (optional but recommended)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create the XGBoost regressor
model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, max_depth=4, learning_rate=0.1)
# model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')

# Train the model
model.fit(X_train, y_train)

# Predict on test set and print RMSE
y_pred = model.predict(X_test)
rmse = mean_squared_error(y_test, y_pred)
print(f"Test RMSE: {rmse:.4f}")

# Save the model to a file
joblib.dump(model, 'xgboost_model.pkl')
print("Model saved as 'xgboost_model.pkl'")
