import os
import pickle
import numpy as np
import pandas as pd

# Path to current folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "knn_model.pkl")
CSV_PATH = os.path.join(BASE_DIR, "nepal_rentals_cleaned.csv")

# Load CSV (used for getting house info)
if os.path.exists(CSV_PATH):
    houses_df = pd.read_csv(CSV_PATH)
else:
    houses_df = None

# Load model
with open(MODEL_PATH, "rb") as f:
    loaded = pickle.load(f)

# Handle different saving formats
if isinstance(loaded, tuple):
    if len(loaded) == 3:
        knn_model, scaler, _ = loaded
    elif len(loaded) == 2:
        knn_model, scaler = loaded
    else:
        knn_model = loaded[0]
        scaler = None
else:
    knn_model = loaded
    scaler = None


def recommend_house(price, beds, baths, n_neighbors=5):
    try:
        if houses_df is None:
            return {"error": "Dataset not found"}

        # Get mean posted_days to use as default for recommendation
        mean_posted_days = houses_df['posted_days'].mean() if 'posted_days' in houses_df.columns else 0

        # Prepare input with 4 features: [price, beds, baths, posted_days]
        input_data = np.array([[price, beds, baths, mean_posted_days]])

        # Scale if scaler exists
        if scaler is not None:
            input_data = scaler.transform(input_data)

        # Get neighbors
        distances, indices = knn_model.kneighbors(
            input_data, n_neighbors=n_neighbors
        )

        recommendations = []

        for idx in indices[0]:
            row = houses_df.iloc[idx]

            recommendations.append({
                "title": row.get("title"),
                "price": row.get("price"),
                "beds": row.get("beds"),
                "baths": row.get("baths"),
                "location": row.get("location"),
                "district": row.get("district"),
                "municipality": row.get("municipality"),
            })

        return recommendations

    except Exception as e:
        return {"error": str(e)}
