import pandas as pd
import numpy as np
import joblib
import os

# =========================================================
# 🤖 AWIS AI MODEL LOADER
# =========================================================
MODEL_PATH = "ml_model/model.pkl"

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None
    print("❌ ERROR: model.pkl not found. Train and save model first.")

# =========================================================
# 🔧 PREPROCESSING FUNCTION
# =========================================================
def preprocess(df):

    df = df.copy()

    # Fill missing values
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna("Unknown")
        else:
            df[col] = df[col].fillna(df[col].median())

    # Convert categorical to numeric
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype("category").cat.codes

    return df

# =========================================================
# 🎯 RISK LEVEL FUNCTION
# =========================================================
def get_risk_level(prob):

    if prob < 30:
        return "LOW 🟢"
    elif prob < 70:
        return "MEDIUM 🟡"
    else:
        return "HIGH 🔴"

# =========================================================
# 🔮 SINGLE EMPLOYEE PREDICTION
# =========================================================
def predict_employee(data_dict):

    """
    Example input:
    {
        "Age": 30,
        "MonthlyIncome": 5000,
        "OverTime": "Yes",
        "Department": "Sales",
        "YearsAtCompany": 3
    }
    """

    if model is None:
        return {"error": "Model not loaded"}

    df = pd.DataFrame([data_dict])
    df_processed = preprocess(df)

    prediction = model.predict(df_processed)[0]

    if hasattr(model, "predict_proba"):
        prob = model.predict_proba(df_processed)[0][1] * 100
    else:
        prob = 50

    return {
        "prediction": int(prediction),
        "risk_probability": round(prob, 2),
        "risk_level": get_risk_level(prob)
    }

# =========================================================
# 📊 BATCH DATASET PREDICTION
# =========================================================
def predict_dataset(df):

    if model is None:
        return None

    df = df.copy()
    df_processed = preprocess(df)

    df["Prediction"] = model.predict(df_processed)

    if hasattr(model, "predict_proba"):
        df["Risk_Probability"] = model.predict_proba(df_processed)[:, 1] * 100
    else:
        df["Risk_Probability"] = 50

    df["Risk_Level"] = df["Risk_Probability"].apply(get_risk_level)

    return df

# =========================================================
# 📌 SUMMARY REPORT FUNCTION
# =========================================================
def generate_summary(df):

    total = len(df)

    high_risk = len(df[df["Risk_Level"] == "HIGH 🔴"])
    medium_risk = len(df[df["Risk_Level"] == "MEDIUM 🟡"])
    low_risk = len(df[df["Risk_Level"] == "LOW 🟢"])

    return {
        "Total Employees": total,
        "High Risk": high_risk,
        "Medium Risk": medium_risk,
        "Low Risk": low_risk
    }

# =========================================================
# 📤 EXPORT RESULT FUNCTION
# =========================================================
def export_results(df, file_type="excel"):

    if file_type == "excel":
        file_path = "awis_prediction.xlsx"
        df.to_excel(file_path, index=False)
        return file_path

    elif file_type == "csv":
        file_path = "awis_prediction.csv"
        df.to_csv(file_path, index=False)
        return file_path

    else:
        file_path = "awis_prediction.txt"
        df.to_string(open(file_path, "w"))
        return file_path