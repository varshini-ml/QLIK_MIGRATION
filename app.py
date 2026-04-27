import streamlit as st
import pandas as pd
# ---------------- CONFIG ----------------
st.set_page_config(page_title="Qlik Migration", layout="wide")
# ---------------- SIDEBAR ----------------
page = st.sidebar.radio("Navigation", ["Upload", "Dashboard", "Insights"])
# ---------------- TITLE ----------------
st.title("🚀 AI-Powered Qlik Migration Assistant")
st.caption("Automated Dashboard Recreation & Insights")
st.markdown("---")
# ---------------- SESSION STATE ----------------
if "data" not in st.session_state:
   st.session_state["data"] = None
# ---------------- UPLOAD PAGE ----------------
if page == "Upload":
   st.subheader("📁 Upload Data")
   uploaded_file = st.file_uploader("Upload CSV (Simulating QVW Data)", type=["csv"])
   if uploaded_file:
       with st.spinner("Analyzing data..."):
           df = pd.read_csv(uploaded_file)
           st.session_state["data"] = df
       st.success("✅ File uploaded successfully!")
   else:
       st.info("Upload a CSV file to generate dashboard")
# ---------------- DASHBOARD PAGE ----------------
elif page == "Dashboard":
   st.subheader("📊 Dashboard")
   if st.session_state["data"] is not None:
       df = st.session_state["data"]
       # -------- FILTER --------
       st.markdown("### 🔍 Filter Data")
       categorical_cols = df.select_dtypes(include=['object']).columns
       if len(categorical_cols) > 0:
           col1, col2 = st.columns(2)
           selected_col = col1.selectbox("Select Column", categorical_cols)
           selected_val = col2.multiselect("Select Values", df[selected_col].unique())
           if selected_val:
               df = df[df[selected_col].isin(selected_val)]
       # -------- DATA PREVIEW --------
       st.markdown("### 📄 Data Preview")
       st.dataframe(df)
       # -------- KPI --------
       st.markdown("### 💡 Key Metrics")
       numeric_cols = df.select_dtypes(include=['number']).columns
       if len(numeric_cols) > 0:
           cols = st.columns(len(numeric_cols))
           for i, col in enumerate(numeric_cols):
               cols[i].metric(col, round(df[col].sum(), 2))
       # -------- CHARTS --------
       st.markdown("### 📊 Visual Insights")
       def suggest_chart(column):
           col = column.lower()
           if "date" in col:
               return "line"
           elif any(x in col for x in ["sales", "revenue", "amount"]):
               return "bar"
           elif any(x in col for x in ["region", "category", "type"]):
               return "pie"
           else:
               return "none"
       for col in df.columns:
           chart = suggest_chart(col)
           if chart == "bar" and col in numeric_cols:
               st.write(f"📊 {col} (Bar Chart)")
               st.bar_chart(df[col])
           elif chart == "line" and col in numeric_cols:
               st.write(f"📈 {col} (Line Chart)")
               st.line_chart(df[col])
           elif chart == "pie":
               st.write(f"🥧 {col} Distribution")
               st.write(df[col].value_counts())
       # -------- DOWNLOAD --------
       st.markdown("### ⬇️ Download Processed Data")
       csv = df.to_csv(index=False).encode('utf-8')
       st.download_button(
           label="Download CSV",
           data=csv,
           file_name='processed_data.csv',
           mime='text/csv',
       )
   else:
       st.warning("⚠️ Please upload data first")
# ---------------- INSIGHTS PAGE ----------------
elif page == "Insights":
   st.subheader("🤖 AI Insights")
   if st.session_state["data"] is not None:
       df = st.session_state["data"]
       numeric_cols = df.select_dtypes(include=['number']).columns
       if len(numeric_cols) > 0:
           for col in numeric_cols:
               st.write(f"📌 {col} average: {round(df[col].mean(), 2)}")
       # EXTRA INSIGHT
       if "Sales" in df.columns and "Region" in df.columns:
           top_region = df.groupby("Region")["Sales"].sum().idxmax()
           st.success(f"🏆 Top performing region: {top_region}")
   else:
       st.warning("⚠️ Upload data first")