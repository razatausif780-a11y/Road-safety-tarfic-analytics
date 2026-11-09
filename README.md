# 🚦 Road Safety & Traffic Incident Analytics
**Developed by Group B (Cronus Consultants Project)**

## 📌 Project Overview
This project is an automated, real-time data analytics pipeline and interactive dashboard developed entirely in Python to identify accident hotspots, understand severity patterns, and monitor emergency response times.

## 🚀 Features
- **Dataset Upload Functionality:** Dynamically upload `accidents.csv` and `responses.csv` via the UI.
- **Hotspot Identification:** Geospatial analysis of high-risk localities.
- **Emergency Response Tracking:** Analyzes EMS dispatch and arrival delays.
- **Live Data Entry:** Insert new accident records dynamically through the UI.

## 💻 Tech Stack
- **Frontend:** Streamlit
- **Data Manipulation:** Pandas, NumPy
- **Data Visualization:** Matplotlib, Seaborn

## ⚙️ How to Run Locally
1. Clone this repository.
2. Install the required libraries: `pip install -r requirements.txt`
3. Run the dashboard: `streamlit run src/app.py`