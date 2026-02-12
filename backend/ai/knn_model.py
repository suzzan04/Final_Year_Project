import pickle
import numpy as np

# Load the model, scaler, and dataframe
with open("ai/knn_model.pkl", "rb") as f:
    model, scaler, df = pickle.load(f)

def recommend_house(price, beds, baths):
    try:
        # We only use the 3 features now
        input_data = np.array([[price, beds, baths]])
        input_scaled = scaler.transform(input_data)

        # Get the 6 closest matches (1st is usually the house itself)
        distances, indices = model.kneighbors(input_scaled)

        # Get the details from the dataframe
        recommended = df.iloc[indices[0]]

        return recommended.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}