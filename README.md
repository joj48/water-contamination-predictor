# 💧 Water Contamination Predictor

This project is a machine learning-powered Streamlit app that predicts water contamination based on key water quality parameters. Built for Smart India Hackathon, it combines modular preprocessing, ethical model deployment, and a user-friendly interface.

## 🚀 Live App

👉 [Launch the App](https://joj48-water-contamination-predictor-streamlit-app-5dtzht.streamlit.app/)

## 📊 Features

- Accepts user input for DO, pH, BOD, Conductivity, Nitrate, and Coliform levels
- Preprocesses inputs using engineered averages and contamination flags
- Predicts contamination using a trained ML model
- Displays results with intuitive feedback (✅ or ⚠️)

## 🛠️ Tech Stack

- Python, scikit-learn, pandas, NumPy
- Streamlit for frontend
- Joblib for model serialization

## 📁 File Structure
         
# Streamlit UI  ├── streamlit_app.py           
# Model loading & preprocessing  ├── predictor.py 
# Trained ML model  ├── contamination_model.pkl        
# Dependencies  ├── requirements.txt

## 🧠 Author

Built by [Jojan Joji](https://github.com/joj48)




