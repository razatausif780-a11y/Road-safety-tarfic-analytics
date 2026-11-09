


# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import os
# from datetime import datetime

# # ==========================================
# # 1. PAGE CONFIGURATION (Sidebar collapsed)
# # ==========================================
# st.set_page_config(page_title="Road Safety & Traffic Analytics", layout="wide", initial_sidebar_state="collapsed")

# # 🔴 FIX: Updated CSS to match Dark Theme perfectly (No more white blanks)
# st.markdown("""
#     <style>
#         div.block-container {padding-top: 2rem;}
#         /* Sleek Dark Metric Cards */
#         .stMetric {
#             background-color: #1e2129; 
#             padding: 15px; 
#             border-radius: 8px; 
#             border-left: 5px solid #00d2d3; 
#             box-shadow: 2px 2px 15px rgba(0,0,0,0.3);
#         }
#         /* Force number text to be bright white */
#         .stMetric [data-testid="stMetricValue"] {
#             color: #ffffff; 
#         }
#         /* Style for the expandable form box */
#         div[data-testid="stForm"] {
#             background-color: #1e2129;
#             border-radius: 10px;
#             padding: 15px;
#             border: 1px solid #333333;
#         }
#     </style>
# """, unsafe_allow_html=True)

# # ==========================================
# # 2. DATA LOAD & PROCESS FUNCTION
# # ==========================================
# @st.cache_data
# def load_data():
#     accidents = pd.read_csv("../data/raw/accidents.csv")
#     responses = pd.read_csv("../data/raw/responses.csv")
    
#     responses['alert_time'] = pd.to_datetime(responses['alert_time'])
#     responses['arrival_time'] = pd.to_datetime(responses['arrival_time'])
#     responses['response_time_mins'] = (responses['arrival_time'] - responses['alert_time']).dt.total_seconds() / 60
    
#     merged_data = pd.merge(accidents, responses, on='accident_id', how='inner')
#     merged_data['hour'] = pd.to_datetime(merged_data['time'], format='%H:%M').dt.hour
#     return merged_data

# try:
#     df = load_data()
# except Exception as e:
#     st.error("Data missing! Pehle terminal mein 'python generate_new_data.py' run karo.")
#     st.stop()

# # ==========================================
# # 3. 🎯 TOP NAVIGATION & FILTERS
# # ==========================================
# st.title("🚦 Road Safety & Incident Command Center")
# st.markdown("---")

# filter_col1, filter_col2, form_col = st.columns([1, 1, 1.5])

# with filter_col1:
#     locality_list = ["All Localities"] + list(df['locality'].unique())
#     selected_locality = st.selectbox("📍 Filter by Locality", locality_list)

# with filter_col2:
#     severity_list = ["All Severities"] + list(df['severity'].unique())
#     selected_severity = st.selectbox("⚠️ Filter by Severity", severity_list)

# with form_col:
#     with st.expander("➕ Report New Accident (Live Entry)", expanded=False):
#         with st.form("new_accident_form", clear_on_submit=True):
#             f_col1, f_col2 = st.columns(2)
#             with f_col1:
#                 new_acc_id = st.text_input("Accident ID (ACC99)")
#                 new_loc = st.selectbox("Locality", df['locality'].unique())
#             with f_col2:
#                 new_type = st.selectbox("Accident Type", df['accident_type'].unique())
#                 new_sev = st.selectbox("Severity", ['Minor', 'Serious', 'Critical', 'Fatal'])
            
#             submit_button = st.form_submit_button("Save to Database", use_container_width=True)

#         if submit_button and new_acc_id:
#             new_record = pd.DataFrame({
#                 'accident_id': [new_acc_id],
#                 'date': [datetime.now().strftime("%Y-%m-%d")],
#                 'time': [datetime.now().strftime("%H:%M")],
#                 'locality': [new_loc],
#                 'accident_type': [new_type],
#                 'severity': [new_sev],
#                 'fatalities': [0],
#                 'injuries': [1]
#             })
#             file_path = os.path.join("..", "data", "raw", "accidents.csv")
#             new_record.to_csv(file_path, mode='a', header=False, index=False)
#             st.success(f"✅ Alert! New {new_sev} accident registered at {new_loc}.")

# # ==========================================
# # 5. ⚙️ APPLY FILTERS
# # ==========================================
# if selected_locality != "All Localities":
#     df = df[df['locality'] == selected_locality]
# if selected_severity != "All Severities":
#     df = df[df['severity'] == selected_severity]

# # ==========================================
# # 6. 📊 MAIN DASHBOARD UI (KPIs)
# # ==========================================
# st.markdown("<br>", unsafe_allow_html=True)
# col1, col2, col3, col4 = st.columns(4)
# col1.metric("Total Accidents", f"{len(df):,}")
# col2.metric("Total Fatalities", f"{df['fatalities'].sum():,}")
# col3.metric("Total Injuries", f"{df['injuries'].sum():,}")
# col4.metric("Avg Response Time", f"{df['response_time_mins'].mean():.1f} Mins")

# st.markdown("---")

# # Setup text color for charts to be visible on dark background
# sns.set_theme(style="darkgrid", rc={"text.color": "#e0e0e0", "axes.labelcolor": "#e0e0e0", "xtick.color": "#e0e0e0", "ytick.color": "#e0e0e0"})

# # ==========================================
# # 7. 📈 CHARTS 
# # ==========================================
# c1, c2, c3 = st.columns(3)

# with c1:
#     st.markdown("**💥 Accidents by Severity**")
#     fig1, ax1 = plt.subplots(figsize=(5, 3.5))
#     sns.countplot(data=df, x='severity', hue='severity', palette=['#10ac84', '#ff9f43', '#ff5e57', '#833471'], 
#                   order=['Minor', 'Serious', 'Critical', 'Fatal'], ax=ax1, legend=False)
#     ax1.set_ylabel("Count")
#     ax1.set_xlabel("")
#     fig1.patch.set_alpha(0.0)
#     ax1.patch.set_alpha(0.0)
#     st.pyplot(fig1)

# with c2:
#     st.markdown("**🏍️ Accident Types**")
#     fig2, ax2 = plt.subplots(figsize=(5, 3.5))
#     sns.countplot(data=df, y='accident_type', hue='accident_type', palette='cool', ax=ax2, legend=False)
#     ax2.set_ylabel("")
#     ax2.set_xlabel("Count")
#     fig2.patch.set_alpha(0.0)
#     ax2.patch.set_alpha(0.0)
#     st.pyplot(fig2)

# with c3:
#     st.markdown("**📍 Hotspots (By Locality)**")
#     fig3, ax3 = plt.subplots(figsize=(5, 3.5))
#     sns.countplot(data=df, x='locality', hue='locality', palette='viridis', ax=ax3, legend=False)
#     plt.xticks(rotation=45)
#     ax3.set_ylabel("Count")
#     ax3.set_xlabel("")
#     fig3.patch.set_alpha(0.0)
#     ax3.patch.set_alpha(0.0)
#     st.pyplot(fig3)

# st.markdown("---")
# c4, c5 = st.columns([2, 1])

# with c4:
#     st.markdown("**⏱️ Hourly Incident Trend (Time Pattern)**")
#     hourly_trend = df.groupby('hour').size().reset_index(name='count')
#     hourly_trend['hour'] = hourly_trend['hour'].astype(str) + ":00"
#     hourly_trend.set_index('hour', inplace=True)
#     st.area_chart(hourly_trend['count'], color="#00d2d3") 

# with c5:
#     st.markdown("**🚑 Avg Response Time (Mins)**")
#     fig5, ax5 = plt.subplots(figsize=(4, 3.5))
#     resp_trend = df.groupby('locality')['response_time_mins'].mean().sort_values().reset_index()
#     sns.barplot(data=resp_trend, x='response_time_mins', y='locality', hue='locality', palette='flare', ax=ax5, legend=False)
#     ax5.set_ylabel("")
#     ax5.set_xlabel("Minutes")
#     fig5.patch.set_alpha(0.0)
#     ax5.patch.set_alpha(0.0)
#     st.pyplot(fig5)

# st.markdown("---")
# st.markdown("**📋 Live Accident Records Database**")
# st.dataframe(df[['accident_id', 'date', 'time', 'locality', 'accident_type', 'severity', 'response_time_mins']].head(15), use_container_width=True)












import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="Road Safety Analytics", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for Sleek Metric Cards and Form
st.markdown("""
    <style>
        div.block-container {padding-top: 2rem;}
        .stMetric {
            background-color: #1e2129; 
            padding: 15px; 
            border-radius: 8px; 
            border-left: 5px solid #00d2d3; 
            box-shadow: 2px 2px 15px rgba(0,0,0,0.3);
        }
        .stMetric [data-testid="stMetricValue"] { color: #ffffff; }
        div[data-testid="stForm"] {
            background-color: #1e2129;
            border-radius: 10px;
            padding: 15px;
            border: 1px solid #333333;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🚦 Road Safety & Incident Command Center")
st.markdown("---")

# ==========================================
# 2. DATASET UPLOAD FUNCTIONALITY (New Requirement)
# ==========================================
st.markdown("### 📂 Upload Datasets to Begin Analysis")
st.info("As per project guidelines, please upload the generated 'accidents.csv' and 'responses.csv' files.")

upload_col1, upload_col2 = st.columns(2)
with upload_col1:
    acc_file = st.file_uploader("Upload accidents.csv", type=['csv'])
with upload_col2:
    res_file = st.file_uploader("Upload responses.csv", type=['csv'])

# Wait for both files to be uploaded before showing the dashboard
if not (acc_file and res_file):
    st.warning("⏳ Waiting for both datasets to be uploaded...")
    st.stop()

# ==========================================
# 3. DATA PROCESS FUNCTION
# ==========================================
@st.cache_data
def load_and_process_data(acc_csv, res_csv):
    accidents = pd.read_csv(acc_csv)
    responses = pd.read_csv(res_csv)
    
    responses['alert_time'] = pd.to_datetime(responses['alert_time'])
    responses['arrival_time'] = pd.to_datetime(responses['arrival_time'])
    responses['response_time_mins'] = (responses['arrival_time'] - responses['alert_time']).dt.total_seconds() / 60
    
    merged_data = pd.merge(accidents, responses, on='accident_id', how='inner')
    merged_data['hour'] = pd.to_datetime(merged_data['time'], format='%H:%M').dt.hour
    return merged_data

# Load data into session state so live entry works smoothly
if 'df' not in st.session_state:
    st.session_state.df = load_and_process_data(acc_file, res_file)

df = st.session_state.df

# ==========================================
# 4. 🎯 TOP NAVIGATION & FILTERS
# ==========================================
filter_col1, filter_col2, form_col = st.columns([1, 1, 1.5])

with filter_col1:
    locality_list = ["All Localities"] + list(df['locality'].unique())
    selected_locality = st.selectbox("📍 Filter by Locality", locality_list)

with filter_col2:
    severity_list = ["All Severities"] + list(df['severity'].unique())
    selected_severity = st.selectbox("⚠️ Filter by Severity", severity_list)

with form_col:
    with st.expander("➕ Report New Accident (Live Entry)", expanded=False):
        with st.form("new_accident_form", clear_on_submit=True):
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                new_acc_id = st.text_input("Accident ID (ACC99)")
                new_loc = st.selectbox("Locality", df['locality'].unique())
            with f_col2:
                new_type = st.selectbox("Accident Type", df['accident_type'].unique())
                new_sev = st.selectbox("Severity", ['Minor', 'Serious', 'Critical', 'Fatal'])
            
            submit_button = st.form_submit_button("Save to Live Database", use_container_width=True)

        if submit_button and new_acc_id:
            # Create a new record and append it dynamically to the current session dataframe
            new_record = pd.DataFrame({
                'accident_id': [new_acc_id],
                'date': [datetime.now().strftime("%Y-%m-%d")],
                'time': [datetime.now().strftime("%H:%M")],
                'locality': [new_loc],
                'accident_type': [new_type],
                'severity': [new_sev],
                'fatalities': [0],
                'injuries': [1],
                'response_time_mins': [15.0], # Default estimated response
                'hour': [datetime.now().hour]
            })
            st.session_state.df = pd.concat([st.session_state.df, new_record], ignore_index=True)
            st.success(f"✅ Alert! New {new_sev} accident registered at {new_loc}.")
            st.rerun()

# Apply Filters
if selected_locality != "All Localities":
    df = df[df['locality'] == selected_locality]
if selected_severity != "All Severities":
    df = df[df['severity'] == selected_severity]

# ==========================================
# 5. 📊 MAIN DASHBOARD UI (KPIs)
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Accidents", f"{len(df):,}")
col2.metric("Total Fatalities", f"{df['fatalities'].sum():,}")
col3.metric("Total Injuries", f"{df['injuries'].sum():,}")
col4.metric("Avg Response Time", f"{df['response_time_mins'].mean():.1f} Mins")

st.markdown("---")

sns.set_theme(style="darkgrid", rc={"text.color": "#e0e0e0", "axes.labelcolor": "#e0e0e0", "xtick.color": "#e0e0e0", "ytick.color": "#e0e0e0"})

# ==========================================
# 6. 📈 CHARTS & VISUALIZATIONS
# ==========================================
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("**💥 Accidents by Severity**")
    fig1, ax1 = plt.subplots(figsize=(5, 3.5))
    sns.countplot(data=df, x='severity', hue='severity', palette=['#10ac84', '#ff9f43', '#ff5e57', '#833471'], 
                  order=['Minor', 'Serious', 'Critical', 'Fatal'], ax=ax1, legend=False)
    ax1.set_ylabel("Count")
    ax1.set_xlabel("")
    fig1.patch.set_alpha(0.0)
    ax1.patch.set_alpha(0.0)
    st.pyplot(fig1)

with c2:
    st.markdown("**🏍️ Accident Types**")
    fig2, ax2 = plt.subplots(figsize=(5, 3.5))
    sns.countplot(data=df, y='accident_type', hue='accident_type', palette='cool', ax=ax2, legend=False)
    ax2.set_ylabel("")
    ax2.set_xlabel("Count")
    fig2.patch.set_alpha(0.0)
    ax2.patch.set_alpha(0.0)
    st.pyplot(fig2)

with c3:
    st.markdown("**📍 Hotspots (By Locality)**")
    fig3, ax3 = plt.subplots(figsize=(5, 3.5))
    sns.countplot(data=df, x='locality', hue='locality', palette='viridis', ax=ax3, legend=False)
    plt.xticks(rotation=45)
    ax3.set_ylabel("Count")
    ax3.set_xlabel("")
    fig3.patch.set_alpha(0.0)
    ax3.patch.set_alpha(0.0)
    st.pyplot(fig3)

st.markdown("---")
c4, c5 = st.columns([2, 1])

with c4:
    st.markdown("**⏱️ Hourly Incident Trend (Time Pattern)**")
    
    # Data group karna
    hourly_trend = df.groupby('hour').size().reset_index(name='count')
    
    # Pandas Trick: Hour ko ek proper "Time" (Datetime) me badalna taaki Streamlit smart formatting kare
    hourly_trend['Time'] = pd.to_datetime(hourly_trend['hour'], format='%H')
    hourly_trend.set_index('Time', inplace=True)
    
    # Streamlit ka native Area Chart (Jisme Zoom, Pan aur Hover kaam karta hai)
    st.area_chart(hourly_trend['count'], color="#00d2d3")

with c5:
    st.markdown("**🚑 Avg Response Time (Mins)**")
    fig5, ax5 = plt.subplots(figsize=(4, 3.5))
    resp_trend = df.groupby('locality')['response_time_mins'].mean().sort_values().reset_index()
    sns.barplot(data=resp_trend, x='response_time_mins', y='locality', hue='locality', palette='flare', ax=ax5, legend=False)
    ax5.set_ylabel("")
    ax5.set_xlabel("Minutes")
    fig5.patch.set_alpha(0.0)
    ax5.patch.set_alpha(0.0)
    st.pyplot(fig5)

st.markdown("---")
st.markdown("**📋 Live Accident Records Database**")
st.dataframe(df[['accident_id', 'date', 'time', 'locality', 'accident_type', 'severity', 'response_time_mins']].head(15), use_container_width=True)