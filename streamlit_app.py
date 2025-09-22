# streamlit_app.py
import streamlit as st
import pandas as pd

# Import your existing prediction logic
from predictor import predict_contamination

# --- Page Configuration ---
st.set_page_config(
    page_title="Water Contamination Predictor",
    page_icon="💧",
    layout="centered"
)

# --- App Title ---
st.title("💧 Water Contamination Predictor")
st.markdown("Choose to predict for a single sample or upload a CSV for batch predictions.")

# --- UI Tabs ---
tab1, tab2 = st.tabs(["**Single Prediction**", "**Batch Prediction (CSV)**"])

# --- Tab 1: Manual Input for a Single Prediction ---
with tab1:
    st.header("Enter Water Quality Parameters:")

    # Using columns for a cleaner layout
    col1, col2 = st.columns(2)

    with col1:
        raw_input = {
            'DO_Min': st.number_input("Dissolved Oxygen Min (mg/L)", min_value=0.0, step=0.1, format="%.2f"),
            'pH_Min': st.number_input("pH Min", min_value=0.0, max_value=14.0, step=0.1, format="%.2f"),
            'Cond_Min': st.number_input("Conductivity Min (µS/cm)", min_value=0.0, step=10.0, format="%.2f"),
            'BOD_Min': st.number_input("BOD Min (mg/L)", min_value=0.0, step=0.1, format="%.2f"),
            'Nitrate_Min': st.number_input("Nitrate Min (mg/L)", min_value=0.0, step=0.1, format="%.2f"),
        }
    with col2:
        raw_input.update({
            'DO_Max': st.number_input("Dissolved Oxygen Max (mg/L)", min_value=0.0, step=0.1, format="%.2f"),
            'pH_Max': st.number_input("pH Max", min_value=0.0, max_value=14.0, step=0.1, format="%.2f"),
            'Cond_Max': st.number_input("Conductivity Max (µS/cm)", min_value=0.0, step=10.0, format="%.2f"),
            'BOD_Max': st.number_input("BOD Max (mg/L)", min_value=0.0, step=0.1, format="%.2f"),
            'Nitrate_Max': st.number_input("Nitrate Max (mg/L)", min_value=0.0, step=0.1, format="%.2f"),
            'TCol_Max': st.number_input("Total Coliform Max (MPN/100ml)", min_value=0.0, step=1.0, format="%.2f")
        })

    if st.button("Predict Contamination"):
        # Call the prediction function with the dictionary of inputs
        result = predict_contamination(raw_input)

        if result == 1:
            st.error("### ⚠️ Result: Contaminated Water Detected")
        else:
            st.success("### ✅ Result: Water is Non-Contaminated")

# --- Tab 2: CSV Upload for Batch Predictions ---
with tab2:
    st.header("Upload a CSV File for Batch Prediction")

    uploaded_file = st.file_uploader(
        "Your CSV file should have the same column names as the manual input fields.",
        type="csv"
    )

    if uploaded_file is not None:
        # Read the uploaded file into a pandas DataFrame
        df = pd.read_csv(uploaded_file)

        st.write("**Uploaded Data Preview:**")
        st.dataframe(df.head())

        if st.button("Run Batch Prediction"):
            with st.spinner('Running predictions...'):
                predictions = []
                # Iterate over each row in the DataFrame
                for index, row in df.iterrows():
                    # Convert row to the dictionary format your model expects
                    row_dict = row.to_dict()
                    # Get prediction for the row
                    prediction = predict_contamination(row_dict)
                    predictions.append(prediction)

                # Add the predictions as a new column to the DataFrame
                df['Prediction'] = predictions
                df['Status'] = df['Prediction'].apply(lambda x: "Contaminated" if x == 1 else "Non-Contaminated")

            st.write("**Prediction Results:**")
            st.dataframe(df)


            # --- Download Button for the Results ---
            # Convert DataFrame to CSV for downloading
            @st.cache_data
            def convert_df_to_csv(df_to_convert):
                return df_to_convert.to_csv(index=False).encode('utf-8')


            csv_results = convert_df_to_csv(df)

            st.download_button(
                label="Download Results as CSV",
                data=csv_results,
                file_name='water_contamination_predictions.csv',
                mime='text/csv',
            )