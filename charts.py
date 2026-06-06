import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "dataset", "cleaned_hr_data.csv")


df = pd.read_csv(DATA_PATH)


def plot_attrition():
    sns.countplot(data=df, x="Attrition")
    plt.title("Attrition Count")
    plt.show()


def plot_department():
    sns.countplot(data=df, x="Department", hue="Attrition")
    plt.title("Department Attrition")
    plt.xticks(rotation=45)
    plt.show()


def plot_income():
    sns.boxplot(data=df, x="Attrition", y="MonthlyIncome")
    plt.title("Income vs Attrition")
    plt.show()


if __name__ == "__main__":
    plot_attrition()
    plot_department()
    plot_income()