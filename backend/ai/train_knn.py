import pandas as pd
import pickle
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

# Load dataset
df = pd.read_csv("ai/nepal_rentals_cleaned.csv")

print("Columns in dataset:", df.columns)

# Use correct feature names from your dataset
features = ["price", "beds", "baths", "posted_days"]

# Remove rows with missing values
df = df.dropna(subset=features)

X = df[features]

# Scale data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train KNN
model = NearestNeighbors(n_neighbors=5)
model.fit(X_scaled)

# Save model
with open("ai/knn_model.pkl", "wb") as f:
    pickle.dump((model, scaler, df), f)

print("✅ KNN model trained and saved successfully!")

