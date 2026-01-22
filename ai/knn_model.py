import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv("dataset.csv")

# Encode categorical columns
le_city = LabelEncoder()
le_type = LabelEncoder()

df["city"] = le_city.fit_transform(df["city"])
df["house_type"] = le_type.fit_transform(df["house_type"])

# Feature selection
X = df[["house_type", "house_size", "city", "price"]]

# Train model
model = NearestNeighbors(n_neighbors=3)
model.fit(X)

def recommend_house(house_type, house_size, city, price):
    input_data = pd.DataFrame([{
        "house_type": house_type,
        "house_size": house_size,
        "city": city,
        "price": price
    }])

    input_data["city"] = le_city.transform(input_data["city"])
    input_data["house_type"] = le_type.transform(input_data["house_type"])

    distances, indices = model.kneighbors(input_data)

    return df.iloc[indices[0]]




if __name__ == "__main__":
    result = recommend_house(
        house_type="Flat",
        house_size=900,
        city="Kathmandu",
        price=15000
    )

    print(result)
