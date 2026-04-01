# =====================================
# 1. IMPORT LIBRARIES
# =====================================
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error, r2_score

# =====================================
# 2. LOAD DATASET
# =====================================
print("Loading dataset...")
df = pd.read_csv("kigali_rent_dataset_100k.csv")
print(f"Dataset Shape: {df.shape}")

# =====================================
# 3. CLEAN DATA
# =====================================
df = df.dropna()
print(f"After dropping NaN: {df.shape}")

# =====================================
# 4. SELECT FEATURES
# =====================================
feature_columns = [
    'size_m2', 
    'year_built', 
    'num_rooms', 
    'near_main_road', 
    'water_available', 
    'electricity_available'
]

# Add location (will be one-hot encoded)
X = df[feature_columns + ['location']].copy()
y = df['rent_price_rwf']

print(f"\nFeatures used: {feature_columns + ['location']}")
print(f"Target: rent_price_rwf")

# =====================================
# 5. CREATE PRICE CATEGORY
# =====================================
def categorize_rent(price):
    if price < 200000:
        return "Low"
    elif price < 600000:
        return "Medium"
    else:
        return "High"

df["rent_category"] = df["rent_price_rwf"].apply(categorize_rent)

# =====================================
# 6. HANDLE CATEGORICAL FEATURES
# =====================================
X = pd.get_dummies(X, columns=['location'])

# Save column names
columns = X.columns.tolist()
print(f"\nTotal features after encoding: {len(columns)}")

# =====================================
# 7. TRAIN / TEST SPLIT
# =====================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =====================================
# 8. FEATURE SCALING
# =====================================
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# =====================================
# 9. TRAIN MODELS
# =====================================
models = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(alpha=1.0),
    "Lasso Regression": Lasso(alpha=0.1)
}

results = {}
best_model = None
best_r2 = -999

print("\n" + "="*50)
print("TRAINING MODELS")
print("="*50)

for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    preds = model.predict(X_test_scaled)

    mse = mean_squared_error(y_test, preds)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, preds)

    results[name] = {"RMSE": rmse, "R2": r2}

    print(f"\n{name}:")
    print(f"  RMSE: {rmse:,.2f} RWF")
    print(f"  R² Score: {r2:.4f}")

    if r2 > best_r2:
        best_r2 = r2
        best_model = model

print(f"\n✅ Best model: {type(best_model).__name__} with R² = {best_r2:.4f}")

# =====================================
# 10. SAVE MODEL + SCALER + COLUMNS
# =====================================
with open("rent_model.pkl", "wb") as f:
    pickle.dump(best_model, f)

with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

with open("columns.pkl", "wb") as f:
    pickle.dump(columns, f)

print("\n✅ Model files saved successfully!")
print("   - rent_model.pkl")
print("   - scaler.pkl") 
print("   - columns.pkl")