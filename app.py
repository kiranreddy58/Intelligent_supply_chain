
import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Intelligent Supply Chain Dashboard",
    page_icon="📦",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("data/raw/supply_chain_dataset1.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df


df = load_data()

# --------------------------------------------------
# DASHBOARD TITLE
# --------------------------------------------------

st.title("📦 Intelligent Supply Chain and Inventory Management")

st.markdown("""
### Project Overview

This system helps monitor and analyze supply chain operations
using data analytics and machine learning.

**Key Features:**
- Inventory monitoring and reorder recommendations
- Demand prediction using Machine Learning
- Warehouse performance analysis
- Supplier lead-time analysis
- Automated inventory recommendations
""")

st.info(
    "Use the sidebar to explore the different modules of the system."
)

st.divider()

# --------------------------------------------------
# LATEST INVENTORY SNAPSHOT
# --------------------------------------------------

latest_date = df["Date"].max()
latest = df[df["Date"] == latest_date]

# --------------------------------------------------
# KEY PERFORMANCE INDICATORS
# --------------------------------------------------

total_skus = df["SKU_ID"].nunique()
total_warehouses = df["Warehouse_ID"].nunique()
total_sales = df["Units_Sold"].sum()
current_inventory = latest["Inventory_Level"].sum()

st.subheader("📊 Supply Chain Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Products",
    f"{total_skus:,}"
)

col2.metric(
    "Total Warehouses",
    f"{total_warehouses:,}"
)

col3.metric(
    "Total Units Sold",
    f"{total_sales:,.0f}"
)

col4.metric(
    "Current Inventory",
    f"{current_inventory:,.0f}"
)

st.divider()

# --------------------------------------------------
# DAILY SALES TREND
# --------------------------------------------------

st.subheader("📈 Daily Sales Trend")

daily_sales = df.groupby(
    "Date",
    as_index=False
)["Units_Sold"].sum()

fig1 = px.line(
    daily_sales,
    x="Date",
    y="Units_Sold",
    title="Daily Units Sold",
    markers=True,
    labels={
        "Date": "Date",
        "Units_Sold": "Units Sold"
    }
)

fig1.update_layout(
    template="plotly_white",
    hovermode="x unified"
)

st.plotly_chart(fig1, width="stretch")

st.divider()

# --------------------------------------------------
# INVENTORY BY WAREHOUSE
# --------------------------------------------------

st.subheader("🏭 Inventory by Warehouse")

warehouse_data = latest.groupby(
    "Warehouse_ID",
    as_index=False
)["Inventory_Level"].sum()

fig2 = px.bar(
    warehouse_data,
    x="Warehouse_ID",
    y="Inventory_Level",
    title="Latest Inventory by Warehouse",
    color="Warehouse_ID",
    labels={
        "Warehouse_ID": "Warehouse",
        "Inventory_Level": "Inventory Units"
    },
    text_auto=True
)

fig2.update_layout(
    template="plotly_white",
    showlegend=False
)

st.plotly_chart(fig2, width="stretch")

st.divider()

# --------------------------------------------------
# DATASET PREVIEW
# --------------------------------------------------

st.subheader("📋 Dataset Preview")

st.write(
    "The following table displays the first 10 records "
    "from the supply chain dataset."
)

st.dataframe(
    df.head(10),
    width="stretch"
)

st.divider()

# --------------------------------------------------
# DATASET INFORMATION
# --------------------------------------------------

st.subheader("📁 Dataset Information")

info1, info2, info3, info4 = st.columns(4)

info1.metric(
    "Total Records",
    f"{len(df):,}"
)

info2.metric(
    "Total Columns",
    len(df.columns)
)

info3.metric(
    "Unique Suppliers",
    df["Supplier_ID"].nunique()
)

info4.metric(
    "Regions",
    df["Region"].nunique()
)

st.write(
    f"**Dataset Period:** {df['Date'].min().date()} "
    f"to {df['Date'].max().date()}"
)

# --------------------------------------------------
# DATA QUALITY CHECK
# --------------------------------------------------

st.subheader("🔍 Data Quality Analysis")

st.write("Missing Values by Column")

missing_values = df.isnull().sum().reset_index()

missing_values.columns = [
    "Column Name",
    "Missing Values"
]

st.dataframe(
    missing_values,
    width="stretch"
)

total_missing = int(df.isnull().sum().sum())

if total_missing == 0:
    st.success("Dataset quality check passed: No missing values found.")
else:
    st.warning(
        f"Dataset contains {total_missing} missing values."
    )

# --------------------------------------------------
# STOCKOUT INFORMATION
# --------------------------------------------------

st.subheader("📦 Stockout Information")

total_stockouts = int(df["Stockout_Flag"].sum())

st.metric(
    "Recorded Stockout Events",
    f"{total_stockouts:,}"
)

st.caption(
    "Stockout events are calculated from the Stockout_Flag column."
)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    f"Dataset latest date: {latest_date.date()} | "
    "Intelligent Supply Chain and Inventory Management System"
)
