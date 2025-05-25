import pandas as pd
import numpy as np
import random

# Set seed for reproducibility
np.random.seed(42)

# Sample categories
categories = ['fashion', 'tech', 'fitness', 'food', 'travel']

data = []
i = 1
for _ in range(100):
    followers = np.random.randint(1000, 1000000)  # 1k to 1M
    engagement_rate = round(np.random.uniform(0.5, 10.0), 2)  # %
    avg_likes = int(followers * (engagement_rate / 100) * np.random.uniform(0.3, 0.8))
    avg_comments = int(avg_likes * np.random.uniform(0.02, 0.1))
    category = random.choice(categories)

    # Label: efficient if engagement > 4.5% and likes > 2k
    efficiency_score = int(engagement_rate > 4.5 and avg_likes > 2000)
    name = "Influencer_"+str(i)
    i +=1
    data.append([
        name, followers, engagement_rate, avg_likes, avg_comments, category, efficiency_score
    ])

# Create DataFrame
df = pd.DataFrame(data, columns=[
    'Influencer_name', 'followers', 'engagement_rate', 'avg_likes', 'avg_comments', 'category', 'efficiency_score'
])

# Save to CSV
df.to_csv('influencer_dataset.csv', index=False)
print("✅ Dataset generated and saved as influencer_dataset.csv")
