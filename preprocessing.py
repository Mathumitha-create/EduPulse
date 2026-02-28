import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans

# 1️⃣ Load dataset
df = pd.read_csv("data/dataset.csv")

# 2️⃣ Drop rows with missing values (drop from full dataframe)
df = df.dropna()

# 3️⃣ Drop target column
df_features = df.drop(columns=["Exam_Score"])

# 4️⃣ Separate categorical and numerical columns
categorical_cols = df_features.select_dtypes(include=["object"]).columns
numerical_cols = df_features.select_dtypes(include=["int64", "float64"]).columns

# 5️⃣ Encode categorical columns
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df_features[col] = le.fit_transform(df_features[col])
    label_encoders[col] = le

# 6️⃣ Scale numerical features
scaler = StandardScaler()
df_features[numerical_cols] = scaler.fit_transform(df_features[numerical_cols])

# 7️⃣ Apply KMeans clustering
kmeans = KMeans(n_clusters=4, random_state=42)
df["Cluster"] = kmeans.fit_predict(df_features)

# 8️⃣ Save processed dataset
df.to_csv("processed_dataset.csv", index=False)

print("✅ Preprocessing & Clustering Completed Successfully")
print(df["Cluster"].value_counts())