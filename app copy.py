import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
# from streamlit_lottie import st_lottie  # Removed since JSON file was missing
import json
import time

# Set Streamlit page config
st.set_page_config(page_title="E-Commerce Delivery Prediction", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
        html, body {
            background: #f4f6f8;
            font-family: 'Segoe UI', sans-serif;
        }
        .main-title {
            text-align: center;
            color: #333;
        }
        .prediction-box {
            padding: 2rem;
            background-color: #ffffff;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            text-align: center;
            margin-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- Load model ---
# Commented out Lottie since file not found
# def load_lottie(filepath):
#     with open(filepath, "r") as f:
#         return json.load(f)

# lottie_animation = load_lottie("project 2.json")  # <- File not found, so removed
model = joblib.load("ecommerce_delivery_pipeline.pkl")

# --- Sidebar ---
st.sidebar.title("Navigation")
st.sidebar.markdown("Select a section to continue.")

# --- Header ---
st.markdown("<h1 class='main-title'>🚚 E-Commerce Product Delivery Prediction</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Predict whether your product will be delivered on time based on order details</h4>", unsafe_allow_html=True)

# --- Input Form ---
with st.form("prediction_form"):
    st.subheader("📋 Enter Order Details")
    col1, col2 = st.columns(2)
    
    with col1:
        customer_care_calls = st.slider("Customer Care Calls", 0, 10, 2)
        customer_rating = st.slider("Customer Rating", 1, 5, 3)
        cost_of_the_product = st.number_input("Cost of the Product ($)", 10, 500, 100)
        prior_purchases = st.slider("Prior Purchases", 0, 20, 5)

    with col2:
        discount = st.slider("Discount Offered (%)", 0, 100, 10)
        weight = st.number_input("Weight in grams", 100, 10000, 500)
        warehouse = st.selectbox("Warehouse Block", ['A', 'B', 'C', 'D', 'F'])
        mode = st.selectbox("Mode of Shipment", ['Flight', 'Ship', 'Road'])

    submit = st.form_submit_button("Predict Delivery Status")

# --- Prediction ---
if submit:
    with st.spinner("Analyzing your input and predicting..."):
        input_data = pd.DataFrame({
            'Customer_care_calls': [customer_care_calls],
            'Customer_rating': [customer_rating],
            'Cost_of_the_Product': [cost_of_the_product],
            'Prior_purchases': [prior_purchases],
            'Discount_offered': [discount],
            'Weight_in_gms': [weight],
            'Warehouse_block': [warehouse],
            'Mode_of_Shipment': [mode]
        })

        prediction = model.predict(input_data)[0]
        result_text = "✅ Delivered on Time" if prediction == 1 else "❌ Delayed"
        color = "#4CAF50" if prediction == 1 else "#FF6B6B"

        st.markdown(f"""
            <div class='prediction-box' style='border-left: 8px solid {color};'>
                <h2>Prediction Result</h2>
                <h1 style='color: {color};'>{result_text}</h1>
            </div>
        """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
---
Made with ❤️ by an Intern · [GitHub](#) · [Contact](#)
""")
