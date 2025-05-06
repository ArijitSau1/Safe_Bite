import streamlit as st
import pandas as pd
import requests

API_URL = "http://127.0.0.1:5000/predict"

# Custom page config
st.set_page_config(page_title="SafeBite - Allergen Detector", page_icon="🍴", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f4f4f4;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: #e63946;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #555;
    }
    .footer {
        text-align: center;
        font-size: 14px;
        color: #888;
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<div class='title'>🍴 SafeBite: Allergen Detection in Food</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Enter food details below to assess allergen risk 🚨</div><br>", unsafe_allow_html=True)

with st.container():
    with st.form("input_form"):
        col1, col2 = st.columns(2)

        with col1:
            food_product = st.text_input("🍜 Food Product", "Pasta")
            sweetener = st.text_input("🍬 Sweetener", "Sugar")
            price = st.number_input("💲 Price", min_value=0.0, format="%.2f", value=10.0)
            customer_rating = st.slider("⭐ Customer Rating (Out of 5)", 0.0, 5.0, 4.5, 0.1)

        with col2:
            main_ingredient = st.text_input("🌾 Main Ingredient", "Wheat")
            fat_oil = st.text_input("🛢️ Fat/Oil", "Olive Oil")
            seasoning = st.text_input("🧂 Seasoning", "Salt, Oregano")
            allergens = st.text_input("⚠️ Known Allergens", "Gluten")

        submitted = st.form_submit_button("🔍 Predict Allergen Risk")

    if submitted:
        input_data = {
            "Food Product": food_product,
            "Main Ingredient": main_ingredient,
            "Sweetener": sweetener,
            "Fat/Oil": fat_oil,
            "Seasoning": seasoning,
            "Allergens": allergens,
            "Price ($)": price,
            "Customer rating (Out of 5)": customer_rating
        }

        try:
            response = requests.post(API_URL, json=input_data)
            if response.status_code == 200:
                result = response.json()
                if result["prediction"] == 1:
                    st.error("⚠️ The food is likely to contain **allergens**.")
                else:
                    st.success("✅ The food is unlikely to contain allergens.")
            else:
                st.warning(f"API Error: {response.json().get('error', 'Unknown error')}")

        except requests.exceptions.RequestException as e:
            st.error(f"Failed to connect to the API: {e}")

# Footer
st.markdown("<div class='footer'>🔬 Developed by <strong>Arijit</strong> | SafeBite 2025</div>", unsafe_allow_html=True)



