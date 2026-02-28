import pandas as pd
import numpy as np

# Load processed dataset
df = pd.read_csv("processed_dataset.csv")

# ---------- Convert Categorical Columns to Numeric Scores ----------

# Map involvement levels
involvement_map = {"Low": 1, "Medium": 3, "High": 5}
df["Parental_Involvement"] = df["Parental_Involvement"].map(involvement_map)

# Map internet access
internet_map = {"No": 0, "Yes": 1}
df["Internet_Access"] = df["Internet_Access"].map(internet_map)

# If Physical_Activity is categorical
activity_map = {"Low": 1, "Medium": 3, "High": 5}
if df["Physical_Activity"].dtype == "object":
    df["Physical_Activity"] = df["Physical_Activity"].map(activity_map)

# ---------- Risk Calculations ----------

# 1️⃣ Engagement Risk
df["Engagement_Risk"] = (
    (100 - df["Attendance"]) * 0.5 +
    (10 - df["Hours_Studied"]) * 5
)

# 2️⃣ Academic Risk
df["Academic_Risk"] = (100 - df["Previous_Scores"]) * 0.6

# 3️⃣ Lifestyle Risk
df["Lifestyle_Risk"] = (
    (8 - df["Sleep_Hours"]) * 5 +
    (5 - df["Physical_Activity"]) * 5
)

# 4️⃣ Environment Risk
df["Environment_Risk"] = (
    (5 - df["Parental_Involvement"]) * 5 +
    (1 - df["Internet_Access"]) * 20
)

# 5️⃣ Final Risk Score
df["Final_Risk_Score"] = (
    df["Engagement_Risk"] * 0.35 +
    df["Academic_Risk"] * 0.35 +
    df["Lifestyle_Risk"] * 0.15 +
    df["Environment_Risk"] * 0.15
)

df["Final_Risk_Score"] = np.clip(df["Final_Risk_Score"], 0, 100)

# 6️⃣ Risk Category
def categorize(score):
    if score < 30:
        return "Low Risk"
    elif score < 60:
        return "Moderate Risk"
    else:
        return "High Risk"

df["Risk_Category"] = df["Final_Risk_Score"].apply(categorize)

# Save final dataset
df.to_csv("final_dataset.csv", index=False)

print("✅ Risk Scoring Completed Successfully")
print(df["Risk_Category"].value_counts())