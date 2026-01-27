import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder, StandardScaler

# ---------------- Load dataset ----------------
df = pd.read_csv("dataset.csv")
print("Initial rows:", len(df))

# ---------------- Clean dataset ----------------
df = df.drop(columns=["Unnamed: 4"], errors="ignore")

# Clean strings
df["house_type"] = df["house_type"].astype(str).str.strip().str.lower()
df["city"] = df["city"].astype(str).str.strip().str.lower()
df["location"] = df["location"].astype(str).str.strip()

# Fix house_size (remove commas)
df["house_size"] = (
    df["house_size"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .astype(int)
)

df["price"] = df["price"].astype(int)

# ---------------- Encode categorical data ----------------
le_type = LabelEncoder()
le_city = LabelEncoder()

df["house_type"] = le_type.fit_transform(df["house_type"])
df["city"] = le_city.fit_transform(df["city"])

# ---------------- Feature selection ----------------
X = df[["house_type", "house_size", "city", "price"]]

print("Feature matrix shape:", X.shape)
print(X.head())

# ---------------- Scaling ----------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ---------------- Train KNN ----------------
model = NearestNeighbors(n_neighbors=3, metric="euclidean")
model.fit(X_scaled)

# ---------------- Safe encode function ----------------
def safe_encode(encoder, value):
    value = value.strip().lower()
    if value not in encoder.classes_:
        raise ValueError(
            f"'{value}' not found in dataset.\n"
            f"Available options: {list(encoder.classes_)}"
        )
    return encoder.transform([value])[0]

# ---------------- Recommendation Function ----------------
def recommend_house(house_type, house_size, city, price):

    house_type_enc = safe_encode(le_type, house_type)
    city_enc = safe_encode(le_city, city)

    input_df = pd.DataFrame([[
        house_type_enc,
        int(house_size),
        city_enc,
        int(price)
    ]], columns=["house_type", "house_size", "city", "price"])

    input_scaled = scaler.transform(input_df)

    distances, indices = model.kneighbors(input_scaled)

    return df.iloc[indices[0]][
        ["house_type", "house_size", "city", "location", "price"]
    ]

# ---------------- Test ----------------
if __name__ == "__main__":
    print("\nAvailable house types:",
          list(le_type.classes_))

    result = recommend_house(
        house_type="studio",   # MUST match dataset meaning
        house_size=400,
        city="delhi",
        price=22000
    )

    print("\nRecommended Houses:\n")
    print(result)
