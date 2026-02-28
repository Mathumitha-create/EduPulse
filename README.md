# 🎓 EduPulse AI
### Role-Based Academic Risk Intelligence & Personalization Platform

> *Detect early · Understand deeply · Intervene effectively*

---

## 📌 Overview

**EduPulse AI** is an AI-powered academic intelligence platform that proactively identifies student performance risks and delivers personalized intervention insights. Unlike traditional dashboards that focus only on final grades, EduPulse AI analyzes **behavioral, academic, and environmental** factors to compute a multi-dimensional risk score and segment students into meaningful behavioral clusters.

The platform features a **dual-role architecture** — a full institutional dashboard for teachers and a personalized profile for students — powered by unsupervised ML, rule-based risk modeling, and AI-generated natural-language insights.

---

## 🎯 Problem Statement

Educational institutions often identify struggling students **only after performance decline becomes severe**. Most analytics tools rely solely on final grades and lack proactive behavioral modeling.

EduPulse AI addresses this gap by:

- Detecting academic risk **early**, before failure occurs
- Segmenting students based on **behavioral patterns**, not just grades
- Providing **personalized improvement strategies** for each student
- Supporting both **educators and learners** through role-specific dashboards

---

## 🧠 Approach

### 1️⃣ Data Preprocessing
- Missing values removed for dataset consistency
- Categorical variables encoded into numerical representations
- Numerical features standardized for fair clustering contribution

### 2️⃣ Behavioral Clustering (Unsupervised ML)
KMeans clustering segments students into **four behavioral archetypes**:

| Cluster | Profile |
|---|---|
| Cluster 0 | High Achievers |
| Cluster 1 | Engaged Learners |
| Cluster 2 | At-Risk Group |
| Cluster 3 | Disengaged Students |

### 3️⃣ Multi-Factor Risk Scoring Engine
A weighted composite risk score (0–100) is computed from:

| Factor | Weight | Indicators |
|---|---|---|
| Engagement | 35% | Attendance, Study Hours |
| Academic | 35% | Previous Scores |
| Lifestyle | 15% | Sleep Hours, Physical Activity |
| Environment | 15% | Parental Involvement, Internet Access |

Risk is categorized as **Low** (0–30) · **Moderate** (30–60) · **High** (60–100).

### 4️⃣ AI-Generated Insights
Rule-driven logic translates numeric scores into **human-readable explanations** and targeted recommendations — for both institutional trends (Teacher) and personal improvement (Student).

### 5️⃣ Role-Based Dashboard Architecture
The UI dynamically adapts based on user role — no cross-role data leakage.

---

## 🏗 System Architecture

```
Data Layer
    └── Preprocessing Module (encoding + scaling)
            └── Clustering Engine (KMeans)
                    └── Risk Scoring Engine (weighted composite)
                            └── Insight Generator (rule-based AI)
                                    └── Role-Based UI (Streamlit)
                                            ├── Teacher Dashboard
                                            └── Student Dashboard
```

---

## 👨‍🏫 Teacher Dashboard Features

| Feature | Description |
|---|---|
| Executive KPIs | Total students, risk distribution, avg exam score |
| Analytics Charts | Cluster bar, risk donut, attendance vs score scatter |
| High-Risk Alerts | Sorted list of students requiring immediate intervention |
| 🔍 Student Lookup | Select by roll number → radar chart + AI teaching strategy + learning pattern tags |
| Risk Heatmap | Color-coded full cohort table with risk-level filter |
| Institutional AI Recommendations | Data-driven action cards for attendance, study habits, sleep, and performance |
| Cluster Academic Profile | Grouped bar chart comparing clusters across key metrics |
| Add / Update Student | Onboard new students; auto-computes risk score |
| Download Report | Full CSV risk report export |

---

## 👩‍🎓 Student Dashboard Features

| Feature | Description |
|---|---|
| Data Input Form | Sliders for attendance, study hours, sleep, scores, lifestyle factors |
| Risk Score Display | Prominent score card + badge + sub-score breakdown bars |
| Strength & Weakness Radar | 7-dimension chart vs class average |
| AI-Generated Insight | Explains which factors drive the student's risk level |
| Personalized Action Plan | Bulleted improvement recommendations |
| What-If Simulator | Drag sliders → live current vs simulated gauge comparison |

---

## 🤖 ML & AI Integration

| Component | Technology |
|---|---|
| Behavioral Segmentation | KMeans Unsupervised Clustering |
| Risk Estimation | Weighted Composite Scoring Model |
| Insight Generation | Rule-Based AI Explanation Engine |
| Visualization | Plotly (radar, scatter, bar, donut, gauge) |
| UI Framework | Streamlit |

> **Explainability First**: Every risk classification traces back to measurable, interpretable factors — no black-box decisions.

---

## 🚀 Getting Started

### Prerequisites
```
Python 3.9+
```

### Installation
```bash
# Clone the repository
git clone <repo-url>
cd Edupulse-AI

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Run the App
```bash
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

### Data Setup
Ensure `final_dataset.csv` is present in the project root. To regenerate from the raw dataset:
```bash
python preprocessing.py
python risk_scoring.py
```

---

## 📁 Project Structure

```
Edupulse-AI/
├── app.py                  # Main Streamlit application (role-based UI)
├── preprocessing.py        # Data cleaning and feature engineering
├── risk_scoring.py         # Risk computation and categorization
├── analysis.py             # Exploratory analysis utilities
├── final_dataset.csv       # Processed dataset with risk scores and clusters
├── processed_dataset.csv   # Intermediate preprocessed data
├── requirements.txt        # Python dependencies
├── models/                 # Saved ML model artifacts
├── data/                   # Raw input data
└── utils/                  # Shared utility functions
```

---

## ⚖ Ethical Considerations

EduPulse AI is a **decision-support tool**, not a deterministic judgment system.

- ✅ Sensitive demographic attributes are not used for risk decisions
- ✅ Risk scores are **advisory**, not predictive of fixed outcomes
- ✅ Teachers retain full authority over all intervention decisions
- ✅ Transparent explanations reduce algorithmic bias
- ⚠️ Accuracy depends on data quality and honest student input
- ⚠️ Risk weights are domain-informed but may require institutional calibration

---

## 💼 Business Feasibility

EduPulse AI can be deployed as:

- A **SaaS academic analytics platform**
- An **LMS plugin** (Moodle, Canvas, Google Classroom)
- A **school-level performance monitoring tool**

**Revenue models**: Per-student licensing · Institutional SaaS contracts · Performance consulting

---

## 🔮 Future Enhancements

- [ ] Real-time LMS data integration
- [ ] Predictive exam score modeling (regression-based)
- [ ] Adaptive weight learning via reinforcement methods
- [ ] Parent portal integration
- [ ] Cross-institution benchmarking analytics
- [ ] Natural language query interface for teachers

---

## 📊 Assumptions

- Dataset contains structured academic and behavioral indicators
- Risk modeling weights are domain-informed but configurable
- Students interact honestly with input fields
- Teachers use insights for **supportive** intervention, not punitive action

---

## 🌟 Conclusion

EduPulse AI transforms traditional academic reporting into **proactive, explainable, and role-aware intelligence**. By combining behavioral clustering, multi-factor risk modeling, and AI-generated insights within a structured dual-role dashboard, the platform bridges the gap between raw data and actionable educational strategy.

> *A scalable step toward intelligent, personalized, and collaborative learning ecosystems.*

---

<div align="center">

**Built with** &nbsp; [Streamlit](https://streamlit.io) · [Plotly](https://plotly.com) · [scikit-learn](https://scikit-learn.org) · [Pandas](https://pandas.pydata.org)

*EduPulse AI · Education | Behavioral Analytics | Personalization · 2026*

</div>
