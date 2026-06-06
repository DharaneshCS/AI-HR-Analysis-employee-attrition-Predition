import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "dataset", "cleaned_hr_data.csv")

df = pd.read_csv(DATA_PATH)

df_encoded = df.copy()

for col in df_encoded.select_dtypes(include=["object"]).columns:
    df_encoded[col] = df_encoded[col].astype("category").cat.codes


def plot_heatmap():
    plt.figure(figsize=(12,8))
    sns.heatmap(df_encoded.corr(), cmap="coolwarm")
    plt.title("Feature Correlation Heatmap")
    plt.show()


if __name__ == "__main__":
    plot_heatmap()