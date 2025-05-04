# 📊 Personal Garmin Dashboard

**Streamlit app for visualizing personal Garmin activity and health data.**

This dashboard allows users to interactively explore trends in their Garmin data using filters, summary statistics, and dynamic visualizations.

---

## 🚀 Features

- 📅 **Date range filter** with support for Year, Quarter, or Month views
- 🧠 **Days Summary**:
  - Heart Rate, Stress Level, Calories, Steps
  - Light & Intense Activity Time
- 🏃 **Activity Summary**:
  - Sport-specific metrics for Running, Cycling, Swimming, and Walking
  - Total/Active Time, Heart Rate, Calories, Speed, Ascent, Descent
- 📈 **Chart options**: Column, Line, Boxplot
- 🧮 Automatic outlier detection
- 📊 Summary tables with aggregated results
- 🌐 Built with **Streamlit** and **Plotly**

---

## 📁 Input Files

Place the following CSV files in the project root:

- `days_summary.csv`: Daily metrics (e.g. heart rate, steps, activity times)
- `activities.csv`: Activity-level metrics per sport (e.g. duration, heart rate, speed)

---
