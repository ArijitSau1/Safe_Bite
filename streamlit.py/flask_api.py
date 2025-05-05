from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load model and encoder
model = joblib.load(r"C:\Users\ariji\SafeBite\Models\best_knn_model2.pkl")
encoder = joblib.load(r"C:\Users\ariji\SafeBite\Models\encoder2.pkl")

@app.route("/")
def home():
    return "Welcome to SafeBite API!"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        input_df = pd.DataFrame(data, index=[0])

        cat_cols = ['Food Product', 'Main Ingredient', 'Sweetener', 'Fat/Oil', 'Seasoning', 'Allergens']
        numeric_cols = ['Price ($)', 'Customer rating (Out of 5)']

        # Encode categorical
        encoded = encoder.transform(input_df[cat_cols])
        encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out())

        final_input = pd.concat([encoded_df, input_df[numeric_cols]], axis=1)
        final_input = final_input[model.feature_names_in_]

        pred = model.predict(final_input)[0]
        return jsonify({"prediction": int(pred)})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
