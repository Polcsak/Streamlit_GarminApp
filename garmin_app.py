import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime

# Nastavenie stránky
st.set_page_config(page_title='Garmin Report', layout='wide', initial_sidebar_state="expanded")

# Set title for Dashboard
st.title("Personal Garmin Dashboard")
st.markdown("---")

# Sidebar Input Widgets for all graphs in Dashboard
with st.sidebar:

    st.title("Filter Pane")
    st.markdown("---")

    period_select = st.radio("Select Period for analysis",
                              ("Year-Month", "Year-Quarter", "Year"))

    date_selected = st.slider(
        'Select Date:',
        min_value=datetime.date(2023, 1, 1),
        max_value=datetime.date.today(),
        value=(datetime.date(2024, 1, 1), datetime.date.today())
    )

    # Output date parameters
    start_date = date_selected[0]
    end_date = date_selected[1]
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

# ----------------------------------------
# Section 1: Days Summary
# ----------------------------------------
#Header for first section
st.header("Trendline Charts - Days Summary")

# Load and Mapping Dataframe
df_days = pd.read_csv("days_summary.csv")

df_days_mapping = {"hr_avg": "Heart Rate",
                   "stress_avg": "Stress Level",
                   "calories_avg": "Calories",
                   "moderate_activity_time": "Light Activity Time",
                   "vigorous_activity_time": "Intense Activity Time",
                   "steps": "Steps"}

df_days = df_days.rename(columns=df_days_mapping)

# Input Widgets for Days Summary (Above Graphs)
control_col1, control_col2 = st.columns(2)

with control_col1:
    
    # Select Variable
    variable_select_days = st.selectbox("Select Variable for analysis", 
                                        ("Heart Rate", "Stress Level", "Calories", "Light Activity Time", "Intense Activity Time", "Steps"),
                                        key="variable_select_days")

with control_col2:                                        
    #Select Chart Type
    chart_selection_days = st.selectbox("Select the chart type", 
                                    ("Column Chart", "Line Chart", "Boxplot Chart"),
                                    key="chart_select_days")



# Data Transformations and adding of date columns
df_days['day'] = pd.to_datetime(df_days['day'])
df_days["Light Activity Time"] = pd.to_timedelta(df_days["Light Activity Time"]).dt.total_seconds() / 60
df_days["Intense Activity Time"] = pd.to_timedelta(df_days["Intense Activity Time"]).dt.total_seconds() / 60
df_days['Year-Month'] = df_days['day'].dt.strftime('%Y-%m')
df_days['Year-Quarter'] = df_days['day'].dt.to_period('Q').astype(str).str.replace('Q', '-Q')
df_days['Year'] = df_days['day'].dt.strftime('%Y')

# Data Filtering
trend_df_days = df_days[(df_days['day'] >= start_date) & (df_days['day'] <= end_date)]


# Data Aggregation
if variable_select_days in ["Light Activity Time", "Intense Activity Time", "Steps"]:
    grouped_df_days = trend_df_days.groupby(period_select)[variable_select_days].agg(['sum']).reset_index()
    grouped_df_days.columns = [period_select, f"{variable_select_days} (Sum)"]
    y_axis_days = f"{variable_select_days} (Sum)"
else:
    grouped_df_days = trend_df_days.groupby(period_select)[variable_select_days].agg(['mean', 'median']).reset_index()
    grouped_df_days.columns = [period_select, f"{variable_select_days} (Mean)", f"{variable_select_days} (Median)"]
    y_axis_days = f"{variable_select_days} (Mean)"


# --- Trendline Chart and Table for Days Summary ---


col1, col2 = st.columns([3, 3])

with col1:
    if chart_selection_days == "Column Chart":
        fig = px.bar(grouped_df_days, x=period_select, y=y_axis_days, title=f"Column Chart of {variable_select_days}")
        st.plotly_chart(fig)
    elif chart_selection_days == "Line Chart":
        fig = px.line(grouped_df_days, x=period_select, y=y_axis_days, title=f"Line Chart of {variable_select_days}")
        st.plotly_chart(fig)
    else:
        fig = px.box(trend_df_days, x=period_select, y=variable_select_days, title=f"Boxplot of {variable_select_days}")
        st.plotly_chart(fig)

with col2:
    # Count of Outlayers
    outlier_counts_days = []

    for period_value in grouped_df_days[period_select]:
        subset = trend_df_days[trend_df_days[period_select] == period_value][variable_select_days]
        Q1 = subset.quantile(0.25)
        Q3 = subset.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = subset[(subset < lower_bound) | (subset > upper_bound)]
        outlier_counts_days.append(len(outliers))

    grouped_df_days["Outliers Count"] = outlier_counts_days
    st.dataframe(grouped_df_days)

# ----------------------------------------
# Section 2: Activities
# ----------------------------------------

st.markdown("---")
#Header for first section
st.header("Trendline Charts - Activity Summary")
st.markdown("---")

# Input Widgets for Activity Summary (Above Visuals)
control_col1, control_col2 = st.columns(2)

with control_col1:
    variable_select_activities = st.selectbox("Select Variable for analysis", 
                                               ("Total Time", "Active Time", "Maximum Heart Rate", "Average Heart Rate", "Active Calories", "Average Speed", "Maximum Speed", "Ascent", "Descent"),
                                               key="variable_select_activities")
    sport_selection_activities = st.selectbox("Select sport activity", 
                                               ("swimming", "running", "walking", "cycling"),
                                               key="sport_select_activities")

with control_col2:
    chart_selection_activities = st.selectbox("Select the chart type (Activities)", 
                                               ("Column Chart", "Line Chart", "Boxplot Chart"),
                                               key="chart_select_activities")

# Load and Mapping Dataframe
df_activities = pd.read_csv("activities.csv")

activity_columns = ["start_time", "sport", "elapsed_time", "moving_time", "max_hr", "avg_hr", "calories", "avg_speed", "max_speed", "ascent", "descent"]
activity_mapping = {
    "start_time": "Date",
    "sport": "sport",
    "elapsed_time": "Total Time",
    "moving_time": "Active Time",
    "max_hr": "Maximum Heart Rate",
    "avg_hr": "Average Heart Rate",
    "calories": "Active Calories",
    "avg_speed": "Average Speed",
    "max_speed": "Maximum Speed",
    "ascent": "Ascent",
    "descent": "Descent"
}

df_activities = df_activities[activity_columns].rename(columns=activity_mapping)

# Data Transformations and adding of date columns
df_activities['Date'] = pd.to_datetime(df_activities['Date'])
df_activities["Active Time"] = pd.to_timedelta(df_activities["Active Time"]).dt.total_seconds() / 60
df_activities["Total Time"] = pd.to_timedelta(df_activities["Total Time"]).dt.total_seconds() / 60
df_activities['Year-Month'] = df_activities['Date'].dt.strftime('%Y-%m')
df_activities['Year-Quarter'] = df_activities['Date'].dt.to_period('Q').astype(str).str.replace('Q', '-Q')
df_activities['Year'] = df_activities['Date'].dt.strftime('%Y')

# Data Filtering
trend_df_activities = df_activities[(df_activities['Date'] >= start_date) & (df_activities['Date'] <= end_date)]
trend_df_activities = trend_df_activities[trend_df_activities['sport'] == sport_selection_activities]

# Data Aggregation
sum_columns = ["Total Time", "Active Time", "Active Calories"]
mean_columns = ["Maximum Heart Rate", "Average Heart Rate", "Average Speed", "Maximum Speed", "Ascent", "Descent"]

if variable_select_activities in sum_columns:
    grouped_df_activities = trend_df_activities.groupby(period_select)[variable_select_activities].agg(['sum']).reset_index()
    grouped_df_activities.columns = [period_select, f"{variable_select_activities} (Sum)"]
    y_axis_activities = f"{variable_select_activities} (Sum)"
else:
    grouped_df_activities = trend_df_activities.groupby(period_select)[variable_select_activities].agg(['mean', 'median']).reset_index()
    grouped_df_activities.columns = [period_select, f"{variable_select_activities} (Mean)", f"{variable_select_activities} (Median)"]
    y_axis_activities = f"{variable_select_activities} (Mean)"

# Visuals
col1, col2 = st.columns(2)

with col1:
    if chart_selection_activities == "Column Chart":
        fig = px.bar(grouped_df_activities, x=period_select, y=y_axis_activities, title=f"Column Chart of {variable_select_activities}")
        st.plotly_chart(fig)
    elif chart_selection_activities == "Line Chart":
        fig = px.line(grouped_df_activities, x=period_select, y=y_axis_activities, title=f"Line Chart of {variable_select_activities}")
        st.plotly_chart(fig)
    else:
        fig = px.box(trend_df_activities, x=period_select, y=variable_select_activities, title=f"Boxplot of {variable_select_activities}")
        st.plotly_chart(fig)

with col2:
    st.dataframe(grouped_df_activities)
