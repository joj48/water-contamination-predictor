import joblib
import numpy as np

# Load trained model
model = joblib.load("contamination_model.pkl")

def preprocess_input(raw):
    DO_avg = (raw['DO_Min'] + raw['DO_Max']) / 2
    pH_avg = (raw['pH_Min'] + raw['pH_Max']) / 2
    Cond_avg = (raw['Cond_Min'] + raw['Cond_Max']) / 2
    BOD_avg = (raw['BOD_Min'] + raw['BOD_Max']) / 2
    Nitrate_avg = (raw['Nitrate_Min'] + raw['Nitrate_Max']) / 2
    high_coliform = int(raw['TCol_Max'] > 500)
    low_DO = int(DO_avg < 4)
    return np.array([[DO_avg, pH_avg, Cond_avg, BOD_avg, Nitrate_avg, high_coliform, low_DO]])

def predict_contamination(raw_input):
    features = preprocess_input(raw_input)
    return model.predict(features)[0]
if __name__ == "__main__":
    # Sample input dictionary (simulate user input)
    test_input = {
        'DO_Min': 5.2,
        'DO_Max': 7.1,
        'pH_Min': 6.8,
        'pH_Max': 7.4,
        'Cond_Min': 180.0,
        'Cond_Max': 240.0,
        'BOD_Min': 2.5,
        'BOD_Max': 3.8,
        'Nitrate_Min': 1.2,
        'Nitrate_Max': 2.9,
        'TCol_Max': 600.0  # Should trigger high_coliform flag
    }

    result = predict_contamination(test_input)
    print("Prediction:", "Contaminated" if result == 1 else "Non-Contaminated")