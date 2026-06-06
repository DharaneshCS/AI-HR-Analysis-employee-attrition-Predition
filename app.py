import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns



CHART_SIZE = (6.5, 4.2)

def style_chart(ax, title=""):
    ax.set_title(title, fontsize=12, fontweight="bold", color="white")
    ax.tick_params(axis='x', labelsize=9)
    ax.tick_params(axis='y', labelsize=9)
    return ax
# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AWIS AI Workforce Intelligence System",
    layout="wide",
    page_icon="🤖"
)

# ================= DARK THEME =================
st.markdown("""
<style>

/* =========================================================
   🌌 GLOBAL BACKGROUND (BLACK + DEEP GRADIENT)
========================================================= */
.stApp {
    background: radial-gradient(circle at top left, #0b1220, #000000);
    color: #ffffff;
    font-family: 'Segoe UI', sans-serif;
    overflow-x: hidden;
}

/* Smooth scrolling */
html, body {
    scroll-behavior: smooth;
}

/* =========================================================
   📌 HEADINGS (MODERN AI LOOK)
========================================================= */
h1 {
    font-size: 38px;
    font-weight: 800;
    background: linear-gradient(90deg, #00ff88, #00b3ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 10px;
}

h2 {
    font-size: 26px;
    font-weight: 700;
    color: #ffffff;
}

h3 {
    font-size: 20px;
    color: #cbd5e1;
}

/* =========================================================
   📌 SIDEBAR (GLASS + DARK GREEN)
========================================================= */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #050a12, #0f172a);
    border-right: 1px solid #1f2937;
    box-shadow: 2px 0px 20px rgba(0,255,136,0.08);
}

/* Sidebar title */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2 {
    color: #00ff88;
}

/* Sidebar text */
[data-testid="stSidebar"] * {
    color: #e2e8f0;
}

/* =========================================================
   📌 KPI CARDS (GLASS MORPHISM)
========================================================= */
.kpi {
    background: rgba(17, 24, 39, 0.7);
    border: 1px solid rgba(0, 255, 136, 0.2);
    border-radius: 18px;
    padding: 22px;
    text-align: center;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
    transition: all 0.3s ease-in-out;
    backdrop-filter: blur(10px);
}

.kpi:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0px 15px 40px rgba(0,255,136,0.15);
}

/* KPI TITLE COLORS */
.red {
    color: #ff4d4d;
    font-weight: 800;
    font-size: 18px;
    letter-spacing: 1px;
}

.green {
    color: #00ff88;
    font-weight: 800;
    font-size: 18px;
    letter-spacing: 1px;
}

.yellow {
    color: #facc15;
    font-weight: 800;
    font-size: 18px;
    letter-spacing: 1px;
}

/* KPI VALUE */
.kpi h2 {
    font-size: 32px;
    margin-top: 10px;
    font-weight: 900;
    color: #ffffff;
}
            

/* =========================================================
   📊 CHART CONTAINERS
========================================================= */
.element-container {
    background: rgba(255,255,255,0.02);
    padding: 10px;
    border-radius: 12px;
    border: 1px solid rgba(0,255,136,0.05);
}
            

/* =========================================================
   📌 BUTTONS (NEON GREEN STYLE)
========================================================= */
.stButton > button {
    background: linear-gradient(90deg, #00ff88, #00b3ff);
    color: black;
    font-weight: bold;
    border-radius: 12px;
    padding: 10px 18px;
    border: none;
    transition: 0.3s ease-in-out;
}

.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0px 5px 20px rgba(0,255,136,0.4);
}

/* =========================================================
   📌 TABLES
========================================================= */
.dataframe {
    background-color: #0b1220;
    color: white;
}

/* =========================================================
   📌 METRICS BOX
========================================================= */
[data-testid="stMetric"] {
    background: rgba(0,0,0,0.3);
    border: 1px solid rgba(0,255,136,0.2);
    padding: 15px;
    border-radius: 12px;
}

/* =========================================================
   📌 SCROLLBAR (MODERN GREEN)
========================================================= */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #0b1220;
}

::-webkit-scrollbar-thumb {
    background: #00ff88;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #00b3ff;
}

/* =========================================================
   📌 FOOTER STYLE SPACE
========================================================= */
footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# ================= LOAD DATA =================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "notebooks", "IBM_HR_Attrition.csv")
df = pd.read_csv(DATA_PATH)

# ================= METRICS =================
total_emp = len(df)
avg_income = df["MonthlyIncome"].mean()
attrition_rate = df["Attrition"].value_counts(normalize=True)["Yes"] * 100

# ================= SIDEBAR =================
st.sidebar.title("AWIS CONTROL PANEL")

menu = st.sidebar.selectbox(
    "Select Module",
    [
        "🏠 Dashboard",
        "📊 Attrition",
        "🏢 Department",
        "💰 Salary",
        "⏳ Experience",
        "⏰ Overtime",
        "🔥 Correlation",
        "⚠ High Risk"
    ]
)
def generate_text_report(df):

    total_emp = len(df)
    attrition_rate = df["Attrition"].value_counts(normalize=True)["Yes"] * 100
    avg_income = df["MonthlyIncome"].mean()

    high_risk = df[
        (df["OverTime"] == "Yes") &
        (df["MonthlyIncome"] < 5000)
    ].shape[0]

    report = f"""
====================================================
        🤖 AWIS HR INTELLIGENCE REPORT
====================================================

📊 OVERVIEW
----------------------------------------------------
Total Employees     : {total_emp}
Attrition Rate      : {attrition_rate:.2f}%
Average Income      : {avg_income:.0f}
High Risk Employees : {high_risk}

====================================================
🧠 KEY INSIGHTS
----------------------------------------------------
✔ Salary strongly affects attrition
✔ Overtime increases resignation risk
✔ Sales department is most affected
✔ Low salary employees leave frequently
✔ Experience improves retention

====================================================
📌 RECOMMENDATIONS
----------------------------------------------------
✔ Improve salary structure
✔ Reduce overtime workload
✔ Improve engagement programs
✔ Focus on high-risk employees
✔ Strengthen HR strategy

====================================================
"""
    return report
# ================= REPORT =================
st.sidebar.markdown("### REPORT GENERATOR")

report_type = st.sidebar.selectbox(
    "Choose Format",
    ["Excel Report", "Text Report"]
)

if st.sidebar.button("Generate Report"):

    # ================= EXCEL REPORT =================
    if report_type == "Excel Report":
        output = BytesIO()
        df.to_excel(output, index=False)

        st.sidebar.download_button(
            "⬇ Download Excel Report",
            data=output.getvalue(),
            file_name="AWIS_HR_Report.xlsx"
        )

    # ================= TEXT REPORT =================
    else:
        text_data = generate_text_report(df)

        st.sidebar.download_button(
            "⬇ Download Text Report",
            data=text_data,
            file_name="AWIS_HR_Report.txt"
        )
# ================= PROJECT TITLE =================
st.title("🤖 AWIS- AI WORKFORCE INTELLIGENCE SYSTEM")
st.markdown("### AI Powered HR Analytics & Employee Attrition Prediction ")

# =====================================================
# 🏠 DASHBOARD
# =====================================================
if menu == "🏠 Dashboard":

    st.subheader("Employee Overview Module")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"<div style='color:red;font-weight:bold;'>Total Employees</div><h2>{total_emp}</h2>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<div style='color:green;font-weight:bold;'>Avg Salary</div><h2>${avg_income:.0f}</h2>", unsafe_allow_html=True)

    with col3:
        st.markdown(f"<div style='color:gold;font-weight:bold;'>Attrition Rate</div><h2>{attrition_rate:.2f}%</h2>", unsafe_allow_html=True)

    st.markdown("### Attrition Pie Chart")
    fig, ax = plt.subplots()
    df["Attrition"].value_counts().plot.pie(autopct="%1.1f%%", ax=ax)
    st.pyplot(fig)

    st.markdown("### Department Count")
    fig, ax = plt.subplots()
    sns.countplot(data=df, x="Department", ax=ax)
    st.pyplot(fig)

    st.markdown("### Salary Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df["MonthlyIncome"], kde=True, ax=ax)
    st.pyplot(fig)

    st.markdown("""
    ### AI INSIGHTS
    1. Salary strongly impacts retention  
    2. Overtime increases attrition  
    3. Sales department is highest risk  
    4. Experience improves stability  
    5. HR must monitor workforce health  
    """)

# =====================================================
# 📊 ATTRITION
# =====================================================
elif menu == "📊 Attrition":

    st.subheader("Attrition Analysis Module")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"<div style='color:red;font-weight:bold;'>Attrition Rate</div><h2>{attrition_rate:.2f}%</h2>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<div style='color:green;font-weight:bold;'>Employees Left</div><h2>{df[df['Attrition']=='Yes'].shape[0]}</h2>", unsafe_allow_html=True)

    with col3:
        st.markdown(f"<div style='color:gold;font-weight:bold;'>Avg Age</div><h2>{df['Age'].mean():.0f}</h2>", unsafe_allow_html=True)

    st.markdown("### Attrition Count")
    fig, ax = plt.subplots()
    sns.countplot(data=df, x="Attrition", ax=ax)
    st.pyplot(fig)

    st.markdown("### Income vs Attrition")
    fig, ax = plt.subplots()
    sns.boxplot(data=df, x="Attrition", y="MonthlyIncome", ax=ax)
    st.pyplot(fig)

    st.markdown("### Age Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df["Age"], kde=True, ax=ax)
    st.pyplot(fig)

    st.markdown("""
    ### AI INSIGHTS
    1. Low salary increases attrition  
    2. Overtime leads to burnout  
    3. Poor satisfaction increases exit  
    4. Work pressure is major factor  
    5. HR must take action immediately  
    """)

# =====================================================
# 🏢 DEPARTMENT
# =====================================================
elif menu == "🏢 Department":

    st.subheader("Department Analysis Module")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"<div style='color:red;font-weight:bold;'>Departments</div><h2>{df['Department'].nunique()}</h2>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<div style='color:green;font-weight:bold;'>Avg Salary</div><h2>${df['MonthlyIncome'].mean():.0f}</h2>", unsafe_allow_html=True)

    with col3:
        st.markdown(f"<div style='color:gold;font-weight:bold;'>Top Risk Dept</div><h2>{df.groupby('Department')['Attrition'].apply(lambda x: (x=='Yes').mean()).idxmax()}</h2>", unsafe_allow_html=True)

    st.markdown("### Department Attrition")
    fig, ax = plt.subplots()
    sns.countplot(data=df, x="Department", hue="Attrition", ax=ax)
    plt.xticks(rotation=15)
    st.pyplot(fig)

    st.markdown("### Salary by Department")
    fig, ax = plt.subplots()
    sns.barplot(data=df, x="Department", y="MonthlyIncome", ax=ax)
    plt.xticks(rotation=15)
    st.pyplot(fig)

    st.markdown("### Experience by Department")
    fig, ax = plt.subplots()
    sns.boxplot(data=df, x="Department", y="YearsAtCompany", ax=ax)
    st.pyplot(fig)

    st.markdown("""
    ### AI INSIGHTS
    1. Sales has highest attrition  
    2. R&D is most stable  
    3. HR moderate risk  
    4. Salary differs by role  
    5. Culture impacts retention  
    """)

# =====================================================
# 💰 SALARY
# =====================================================
elif menu == "💰 Salary":

    st.subheader("Salary Analysis Module")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"<div style='color:red;font-weight:bold;'>Max Salary</div><h2>${df['MonthlyIncome'].max()}</h2>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<div style='color:green;font-weight:bold;'>Avg Salary</div><h2>${avg_income:.0f}</h2>", unsafe_allow_html=True)

    with col3:
        st.markdown(f"<div style='color:gold;font-weight:bold;'>Min Salary</div><h2>${df['MonthlyIncome'].min()}</h2>", unsafe_allow_html=True)

    st.markdown("### Salary Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df["MonthlyIncome"], kde=True, ax=ax)
    st.pyplot(fig)

    st.markdown("### Salary vs Attrition")
    fig, ax = plt.subplots()
    sns.boxplot(data=df, x="Attrition", y="MonthlyIncome", ax=ax)
    st.pyplot(fig)

    st.markdown("### Salary by Department")
    fig, ax = plt.subplots()
    sns.violinplot(data=df, x="Department", y="MonthlyIncome", ax=ax)
    plt.xticks(rotation=15)
    st.pyplot(fig)

    st.markdown("""
    ### AI INSIGHTS
    1. Low salary increases attrition  
    2. Mid salary = stable employees  
    3. High salary improves retention  
    4. Salary gap reduces morale  
    5. HR must fix compensation structure  
    """)

# =====================================================
# ⏳ EXPERIENCE
# =====================================================
elif menu == "⏳ Experience":

    st.subheader("Experience Analysis Module")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"<div style='color:red;font-weight:bold;'>Avg Years</div><h2>{df['YearsAtCompany'].mean():.1f}</h2>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<div style='color:green;font-weight:bold;'>Max Years</div><h2>{df['YearsAtCompany'].max()}</h2>", unsafe_allow_html=True)

    with col3:
        st.markdown(f"<div style='color:gold;font-weight:bold;'>Min Years</div><h2>{df['YearsAtCompany'].min()}</h2>", unsafe_allow_html=True)

    st.markdown("### Experience Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df["YearsAtCompany"], kde=True, ax=ax)
    st.pyplot(fig)
    
    min_experience = df["YearsAtCompany"].min()
    st.write("Minimum Years of Experience:", min_experience)

    st.markdown("### Experience vs Attrition")
    fig, ax = plt.subplots()
    sns.boxplot(data=df, x="Attrition", y="YearsAtCompany", ax=ax)
    st.pyplot(fig)

    st.markdown("### Experience Trend")
    fig, ax = plt.subplots()
    sns.barplot(data=df, x="Attrition", y="YearsAtCompany", ax=ax)
    st.pyplot(fig)

    st.markdown("""
    ### AI INSIGHTS
    1. New employees leave faster  
    2. First year is critical  
    3. Experience improves retention  
    4. Training reduces attrition  
    5. Long-term employees stay  
    """)

# =====================================================
# ⏰ OVERTIME
# =====================================================
elif menu == "⏰ Overtime":

    st.subheader("Overtime Analysis Module")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"<div style='color:red;font-weight:bold;'>Overtime Yes</div><h2>{df[df['OverTime']=='Yes'].shape[0]}</h2>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<div style='color:green;font-weight:bold;'>Overtime No</div><h2>{df[df['OverTime']=='No'].shape[0]}</h2>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div style='color:gold;font-weight:bold;'>Risk Level</div><h2>HIGH</h2>", unsafe_allow_html=True)

    st.markdown("### Overtime Count")
    fig, ax = plt.subplots()
    sns.countplot(data=df, x="OverTime", hue="Attrition", ax=ax)
    st.pyplot(fig)

    st.markdown("### Income vs Overtime")
    fig, ax = plt.subplots()
    sns.boxplot(data=df, x="OverTime", y="MonthlyIncome", ax=ax)
    st.pyplot(fig)

    st.markdown("### Age Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df["Age"], kde=True, ax=ax)
    st.pyplot(fig)

    st.markdown("""
    ### AI INSIGHTS
    1. Overtime increases burnout  
    2. Work-life imbalance risk  
    3. Stress leads resignation  
    4. HR must reduce workload  
    5. Rest policies needed  
    """)

# =====================================================
# 🔥 CORRELATION
# =====================================================
elif menu == "🔥 Correlation":

    st.subheader("Correlation Module")

    df_encoded = df.copy()
    for col in df_encoded.select_dtypes(include=["object"]).columns:
        df_encoded[col] = df_encoded[col].astype("category").cat.codes

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div style='color:red;font-weight:bold;'>Features</div><h2>{}</h2>".format(len(df.columns)), unsafe_allow_html=True)

    with col2:
        st.markdown("<div style='color:green;font-weight:bold;'>Numeric Fields</div><h2>{}</h2>".format(len(df_encoded.select_dtypes(include=['int64','float64']).columns)), unsafe_allow_html=True)

    with col3:
        st.markdown("<div style='color:gold;font-weight:bold;'>Correlation Active</div><h2>ON</h2>", unsafe_allow_html=True)

    st.markdown("### Correlation Heatmap")
    fig, ax = plt.subplots()
    sns.heatmap(df_encoded.corr(), cmap="Blues", ax=ax)
    st.pyplot(fig)

    st.markdown("### Income vs Experience")
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x="MonthlyIncome", y="YearsAtCompany", ax=ax)
    st.pyplot(fig)

    st.markdown("### Age vs Income")
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x="Age", y="MonthlyIncome", ax=ax)
    st.pyplot(fig)

    st.markdown("""
    ### AI INSIGHTS
    1. Salary impacts attrition  
    2. Overtime increases risk  
    3. Experience reduces exits  
    4. Job satisfaction matters  
    5. Hidden patterns detected  
    """)

# =====================================================
# ⚠ HIGH RISK
# =====================================================
elif menu == "⚠ High Risk":

    st.subheader("High Risk Module")

    risk = df[(df["OverTime"]=="Yes") & (df["MonthlyIncome"]<5000)]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"<div style='color:red;font-weight:bold;'>High Risk</div><h2>{risk.shape[0]}</h2>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<div style='color:green;font-weight:bold;'>Risk %</div><h2>{(risk.shape[0]/len(df))*100:.2f}%</h2>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div style='color:gold;font-weight:bold;'>Alert Level</div><h2>CRITICAL</h2>", unsafe_allow_html=True)

    st.markdown("### Risk Employees")
    st.dataframe(risk)

    st.markdown("### Department Risk")
    fig, ax = plt.subplots()
    sns.countplot(data=risk, x="Department", ax=ax)
    st.pyplot(fig)

    st.markdown("### Income Risk Distribution")
    fig, ax = plt.subplots()
    sns.histplot(risk["MonthlyIncome"], kde=True, ax=ax)
    st.pyplot(fig)

    st.markdown("""
    ### AI INSIGHTS
    1. Low salary + overtime = danger  
    2. Burnout employees leave early  
    3. HR must take action  
    4. Risk detection important  
    5. Retention strategy needed  
    """)