# ml_model/train_model.py

import sys
# Safely reconfigure terminal output to UTF-8 if stdout is available
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from preprocess import preprocess_data


def train_model(data_path):
    print("\n🚀 Loading dataset...")

    # Load data
    df = pd.read_csv(data_path)

    print("🔧 Preprocessing data...")
    # FIXED: Unpack all 3 values returned by your updated preprocess_data function
    X, y, encoders = preprocess_data(df)

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print("🤖 Training model...")

    # Model
    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced"
    )

    model.fit(X_train, y_train)

    print("📊 Evaluating model...")

    # Predict
    y_pred = model.predict(X_test)

    print("\n✅ Accuracy:", accuracy_score(y_test, y_pred))
    print("\n📄 Classification Report:\n", classification_report(y_test, y_pred))
    print("\n📌 Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

    # FIXED: Save both the model AND the encoders dictionary into a single file
    artifacts = {
        "model": model,
        "encoders": encoders
    }
    joblib.dump(artifacts, "model.pkl")
    print("\n💾 Model and categorical encoders saved as model.pkl")


if __name__ == "__main__":
    data_path = "notebooks\\IBM_HR_Attrition.csv"
    train_model(data_path)
