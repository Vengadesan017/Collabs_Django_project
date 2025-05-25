import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv('influencer_dataset.csv')

# Encode category
le = LabelEncoder()
df['category_encoded'] = le.fit_transform(df['category'])

# Features & Target
X = df[['followers', 'engagement_rate', 'avg_likes', 'avg_comments', 'category_encoded']]
y = df['efficiency_score']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
model.fit(X_train, y_train)

# Predict probabilities
df['efficiency_prob'] = model.predict_proba(X)[:, 1]

# Sort influencers by efficiency
df_sorted = df.sort_values(by='efficiency_prob', ascending=False)

# Save sorted result
df_sorted.to_csv('sorted_influencers.csv', index=False)

# Evaluate
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Model trained. Accuracy: {acc:.2f}")
print("Sorted influencers saved to sorted_influencers.csv")

print("""
      ======================\
      
      ======================
      cvfd
      """)
