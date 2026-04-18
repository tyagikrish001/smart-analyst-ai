import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Smart Analyst AI", layout="wide")

# -------------------------------
# 🎯 HEADER
# -------------------------------
st.title("📊 Smart Business Analyst AI")
st.markdown("Analyze your business data with automated insights & recommendations")

# -------------------------------
# 📂 SIDEBAR
# -------------------------------
st.sidebar.header("⚙️ Controls")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip()

        # -------------------------------
        # 🔍 COLUMN SELECTION
        # -------------------------------
        numeric_cols = df.select_dtypes(include='number').columns.tolist()

        if not numeric_cols:
            st.error("No numeric column found")
            st.stop()

        selected_col = st.sidebar.selectbox("Select Metric", numeric_cols)

        # Detect date column
        date_col = None
        for col in df.columns:
            if "date" in col.lower():
                date_col = col
                break

        if date_col:
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

        # -------------------------------
        # 📊 KPI CARDS
        # -------------------------------
        st.subheader("📊 Key Metrics")

        total = df[selected_col].sum()
        avg = df[selected_col].mean()
        max_val = df[selected_col].max()
        min_val = df[selected_col].min()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total", f"{total:.0f}")
        col2.metric("Average", f"{avg:.2f}")
        col3.metric("Max", f"{max_val:.0f}")
        col4.metric("Min", f"{min_val:.0f}")

        # -------------------------------
        # 📈 TREND
        # -------------------------------
        if date_col:
            st.subheader("📈 Trend Analysis")

            trend = df.groupby(date_col)[selected_col].sum()
            trend.index = trend.index.strftime('%d-%b')

            fig, ax = plt.subplots()
            ax.plot(trend.index, trend.values, marker='o')
            ax.set_title("Sales Trend")
            plt.xticks(rotation=45)

            st.pyplot(fig)

        # -------------------------------
        # 📍 CATEGORY ANALYSIS
        # -------------------------------
        st.subheader("📍 Category Analysis")

        cat_col = None
        for col in df.columns:
            if any(x in col.lower() for x in ["city", "region", "category"]):
                cat_col = col
                break

        if cat_col:
            cat_data = df.groupby(cat_col)[selected_col].sum().sort_values(ascending=False)
            st.dataframe(cat_data)

        # -------------------------------
        # 🧠 INSIGHTS
        # -------------------------------
        st.subheader("🧠 Insights")

        if date_col and len(trend) >= 2:
            if trend.iloc[-1] < trend.iloc[0]:
                st.warning("Sales trend is decreasing")

            st.info(f"Peak on: {trend.idxmax()}")
            st.info(f"Lowest on: {trend.idxmin()}")

        # -------------------------------
        # 💡 RECOMMENDATIONS
        # -------------------------------
        st.subheader("💡 Recommendations")

        if cat_col:
            top_loc = df.groupby(cat_col)[selected_col].sum().idxmax()
            st.success(f"Focus on {top_loc}")

        st.write("Improve marketing on low-performing days")

        # -------------------------------
        # 📂 RAW DATA (optional)
        # -------------------------------
        with st.expander("View Raw Data"):
            st.dataframe(df)

    except Exception as e:
        st.error(f"Error: {e}")

else:
    st.info("Upload a CSV file from the sidebar to begin")