from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load model (no encoder needed)
model = joblib.load(r"C:\Users\ariji\SafeBite\Models\best_knn_model2.pkl")

@app.route("/")
def home():
    return "Welcome to SafeBite API!"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON data (must be pre-encoded numerically)
        data = request.get_json()
        input_df = pd.DataFrame(data, index=[0])
        
        # Ensure columns match the model's training data
        # Note: All features must already be numerical (no categorical text)
        final_input = input_df[model.feature_names_in_]
        
        # Predict
        pred = model.predict(final_input)[0]
        return jsonify({"prediction": int(pred)})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)