# train_model.py
import joblib
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PowerTransformer
from sklearn.model_selection import train_test_split, RandomizedSearchCV,StratifiedKFold
from sklearn.linear_model import LogisticRegression
from scipy.stats import loguniform
from sklearn.metrics import classification_report,accuracy_score

df=pd.read_excel(r"C:\Users\jojan\ml-learn-track\iypnb\contamination_analysis_2.xlsx")


features = ['DO_avg', 'pH_avg', 'Cond_avg', 'BOD_avg', 'Nitrate_avg', 'high_coliform', 'low_DO']
X = df[features]
y = df['Contaminated']

# --- Train-test split ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# --- Pipeline and hyperparameter tuning ---
param_dist = {
    'model__C': loguniform(0.001, 10),
    'model__penalty': ['l1', 'l2'],
    'model__solver': ['liblinear']
}

pipe = Pipeline([
    ('yeo', PowerTransformer(method='yeo-johnson')),
    ('scaler', StandardScaler()),
    ('model', LogisticRegression(max_iter=1000))
])
cv_strategy = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
search = RandomizedSearchCV(pipe, param_distributions=param_dist, n_iter=50, cv=cv_strategy, scoring='f1', random_state=42)
search.fit(X_train, y_train)

# --- Evaluation ---
best_model = search.best_estimator_
y_train_pred = best_model.predict(X_train)
y_pred = best_model.predict(X_test)

print("Best Parameters:", search.best_params_)
print(classification_report(y_test, y_pred))
print(accuracy_score(y_train, y_train_pred))
print(accuracy_score(y_test, y_pred))

def
joblib.dump(best_model, "contamination_model.pkl")

