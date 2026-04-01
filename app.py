from flask import Flask, request, jsonify, render_template, send_from_directory
import pickle
import pandas as pd
import numpy as np
from collections import deque

app = Flask(__name__)

# Load model, scaler, and columns
try:
    model = pickle.load(open("rent_model.pkl", "rb"))
    scaler = pickle.load(open("scaler.pkl", "rb"))
    columns = pickle.load(open("columns.pkl", "rb"))
    print("✅ Model loaded successfully!")
    print(f"Model expects {len(columns)} features")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    exit()

# Store prediction history for charts (max 50 predictions)
prediction_history = deque(maxlen=50)
actual_values = []  # For demo purposes - in production you'd collect actual rents

# Price categories
def categorize_rent(price):
    if price < 200000:
        return "Low"
    elif price < 600000:
        return "Medium"
    else:
        return "High"

# Extract available locations from column names
locations = [col.replace("location_", "") for col in columns if col.startswith("location_")]
print(f"Available locations: {len(locations)}")

@app.route("/")
def home():
    return render_template("index.html", locations=locations, developer_name="Onesengineer")

@app.route('/test')
def test_page():
    return send_from_directory('.', 'standalone.html')

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        print(f"Received data: {data}")
        
        # Create input dataframe with ALL required features
        input_data = {}
        
        # Initialize all features to 0
        for col in columns:
            input_data[col] = 0
        
        # Fill in the values from the form
        input_data['size_m2'] = float(data.get('size_m2', 0))
        input_data['year_built'] = int(data.get('year_built', 2000))
        input_data['num_rooms'] = int(data.get('num_rooms', 1))
        input_data['near_main_road'] = int(data.get('near_main_road', 0))
        input_data['water_available'] = int(data.get('water_available', 0))
        input_data['electricity_available'] = int(data.get('electricity_available', 1))
        
        # Set location
        location = data.get('location', '')
        location_col = f"location_{location}"
        if location_col in input_data:
            input_data[location_col] = 1
        
        # Convert to DataFrame
        input_df = pd.DataFrame([input_data])
        
        # Ensure all columns are in correct order
        input_df = input_df[columns]
        
        # Scale the input
        input_scaled = scaler.transform(input_df)
        
        # Make prediction
        prediction = model.predict(input_scaled)[0]
        category = categorize_rent(prediction)
        
        # Store prediction for charts
        prediction_history.append({
            'id': len(prediction_history),
            'predicted': float(prediction),
            'size_m2': data.get('size_m2', 0),
            'num_rooms': data.get('num_rooms', 0),
            'location': location
        })
        
        return jsonify({
            "success": True,
            "predicted_rent": float(prediction),
            "category": category,
            "predicted_rent_formatted": f"{prediction:,.0f} RWF",
            "history": list(prediction_history)
        })
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

@app.route("/history", methods=["GET"])
def get_history():
    """Return prediction history for charts"""
    return jsonify({
        "success": True,
        "history": list(prediction_history)
    })

@app.route("/statistics", methods=["GET"])
def get_statistics():
    """Return statistics about predictions"""
    if len(prediction_history) == 0:
        return jsonify({"success": True, "stats": {}})
    
    predictions = [p['predicted'] for p in prediction_history]
    sizes = [p['size_m2'] for p in prediction_history]
    
    # Calculate correlation between size and price
    if len(predictions) > 1:
        correlation = np.corrcoef(sizes, predictions)[0, 1]
    else:
        correlation = 0
    
    stats = {
        'avg_price': np.mean(predictions),
        'min_price': np.min(predictions),
        'max_price': np.max(predictions),
        'avg_size': np.mean(sizes),
        'total_predictions': len(prediction_history),
        'correlation_size_price': correlation
    }
    
    return jsonify({
        "success": True,
        "stats": stats
    })

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)