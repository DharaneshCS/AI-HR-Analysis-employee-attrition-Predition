# ml_model/preprocess.py

import pandas as pd
from sklearn.preprocessing import LabelEncoder

def preprocess_data(df, encoders=None):
    """
    Clean + encode IBM HR dataset.
    
    Parameters:
    - df: The raw input pandas DataFrame.
    - encoders: A dict of pre-fitted LabelEncoders (used for inference/testing).
                If None, new encoders will be fitted (used for training).
                
    Returns:
    - X (features), y (target), encoders (dict of LabelEncoders)
    """
    # Work on a copy to avoid SettingWithCopyWarning or mutating original data
    df = df.copy()

    # Drop unnecessary columns (safe for IBM dataset)
    drop_cols = [
        "EmployeeNumber",
        "EmployeeCount",
        "StandardHours",
        "Over18"
    ]

    for col in drop_cols:
        if col in df.columns:
            df.drop(col, axis=1, inplace=True)

    # Target column (only process if it exists in the data)
    y = None
    if "Attrition" in df.columns:
        df["Attrition"] = df["Attrition"].map({"Yes": 1, "No": 0})
        y = df["Attrition"]
        df.drop("Attrition", axis=1, inplace=True)

    # Encode categorical columns
    cat_cols = df.select_dtypes(include="object").columns
    
    return_encoders = {} if encoders is None else encoders

    for col in cat_cols:
        if encoders is None:
            # Training Mode: Fit a brand new encoder for this column
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            return_encoders[col] = le
        else:
            # Inference/Testing Mode: Use the existing pre-fit encoder
            if col in encoders:
                df[col] = encoders[col].transform(df[col])
            else:
                raise ValueError(f"No pre-fitted LabelEncoder provided for column: {col}")

    X = df
    return X, y, return_encoders
