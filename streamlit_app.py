import streamlit as st
import pandas as pd
import io

# Import your existing prediction logic
# This is a dummy function for demonstration. Replace with your actual predictor.
from predictor import predict_contamination

# --- Page Configuration ---
st.set_page_config(
    page_title="Water Contamination Predictor",
    page_icon="💧",
    layout="centered"
)

# --- Helper Function for CSV Conversion ---
@st.cache_data
def convert_df_to_csv(df_to_convert):
    """Converts a DataFrame to a CSV string for downloading."""
    return df_to_convert.to_csv(index=False).encode('utf-8')


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
            'DO_Min': st.number_input("Dissolved Oxygen Min (mg/L)", min_value=0.0, step=0.1, format="%.2f", key="single_do_min"),
            'pH_Min': st.number_input("pH Min", min_value=0.0, max_value=14.0, step=0.1, format="%.2f", key="single_ph_min"),
            'Cond_Min': st.number_input("Conductivity Min (µS/cm)", min_value=0.0, step=10.0, format="%.2f", key="single_cond_min"),
            'BOD_Min': st.number_input("BOD Min (mg/L)", min_value=0.0, step=0.1, format="%.2f", key="single_bod_min"),
            'Nitrate_Min': st.number_input("Nitrate Min (mg/L)", min_value=0.0, step=0.1, format="%.2f", key="single_nitrate_min"),
        }
    with col2:
        raw_input.update({
            'DO_Max': st.number_input("Dissolved Oxygen Max (mg/L)", min_value=0.0, step=0.1, format="%.2f", key="single_do_max"),
            'pH_Max': st.number_input("pH Max", min_value=0.0, max_value=14.0, step=0.1, format="%.2f", key="single_ph_max"),
            'Cond_Max': st.number_input("Conductivity Max (µS/cm)", min_value=0.0, step=10.0, format="%.2f", key="single_cond_max"),
            'BOD_Max': st.number_input("BOD Max (mg/L)", min_value=0.0, step=0.1, format="%.2f", key="single_bod_max"),
            'Nitrate_Max': st.number_input("Nitrate Max (mg/L)", min_value=0.0, step=0.1, format="%.2f", key="single_nitrate_max"),
            'TCol_Max': st.number_input("Total Coliform Max (MPN/100ml)", min_value=0.0, step=1.0, format="%.2f", key="single_tcol_max")
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
        df = None
        try:
            # THE FIX: Use 'utf-8-sig' to handle the potential BOM character from Excel.
            df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
        except Exception as e:
             st.error(f"Failed to read the file. Please ensure it's a valid CSV and saved with UTF-8 encoding. Error: {e}")

        if df is not None:
            st.write("**Uploaded Data Preview:**")
            st.dataframe(df.head())

            if st.button("Run Batch Prediction"):
                with st.spinner('Running predictions...'):
                    try:
                        # Use a more efficient .apply() method for predictions
                        predictions = df.apply(predict_contamination, axis=1)
                        df['Prediction'] = predictions
                        df['Status'] = df['Prediction'].apply(lambda x: "Contaminated" if x == 1 else "Non-Contaminated")

                        st.success("Batch prediction complete!")
                        st.write("**Prediction Results:**")
                        st.dataframe(df)

                        # --- Download Button for the Results ---
                        csv_results = convert_df_to_csv(df)

                        st.download_button(
                            label="Download Results as CSV",
                            data=csv_results,
                            file_name='water_contamination_predictions.csv',
                            mime='text/csv',
                        )
                    except Exception as e:
                        st.error(f"An error occurred during prediction. Please check your CSV file's columns match the input fields. Error: {e}")

