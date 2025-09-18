# streamlit_app.py
import streamlit as st# Import your logic
from predictor import predict_contamination

st.title("💧 Water Contamination Predictor")
st.subheader("Enter water quality parameters:")

raw_input = {
    'DO_Min': st.number_input("Dissolved Oxygen Min (mg/L)", min_value=0.0),
    'DO_Max': st.number_input("Dissolved Oxygen Max (mg/L)", min_value=0.0),
    'pH_Min': st.number_input("pH Min", min_value=0.0),
    'pH_Max': st.number_input("pH Max", min_value=0.0),
    'Cond_Min': st.number_input("Conductivity Min (µmho/cm)", min_value=0.0),
    'Cond_Max': st.number_input("Conductivity Max (µmho/cm)", min_value=0.0),
    'BOD_Min': st.number_input("BOD Min (mg/L)", min_value=0.0),
    'BOD_Max': st.number_input("BOD Max (mg/L)", min_value=0.0),
    'Nitrate_Min': st.number_input("Nitrate Min (mg/L)", min_value=0.0),
    'Nitrate_Max': st.number_input("Nitrate Max (mg/L)", min_value=0.0),
    'TCol_Max': st.number_input("Total Coliform Max (MPN/100ml)", min_value=0.0)
}

if st.button("Predict Contamination"):
    result = predict_contamination(raw_input)
    if result == 1:
        st.error("⚠️ Contaminated Water Detected")
    else:
        st.success("✅ Water is Non-Contaminated")