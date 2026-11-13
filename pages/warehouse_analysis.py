
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🏭 Warehouse Analysis")

@st.cache_data
def load_data():
    df = pd.read_csv("data/raw/supply_chain_dataset1.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# Latest inventory snapshot
latest_date = df["Date"].max()
latest = df[df["Date"] == latest_date].copy()

# Warehouse inventory summary
inventory_summary = latest.groupby(
    "Warehouse_ID", as_index=False
).agg(
    Total_Inventory=("Inventory_Level", "sum"),
    Average_Inventory=("Inventory_Level", "mean"),
    Product_Count=("SKU_ID", "nunique")
)

# Warehouse sales summary
sales_summary = df.groupby(
    "Warehouse_ID", as_index=False
).agg(
    Total_Units_Sold=("Units_Sold", "sum"),
    Average_Daily_Sales=("Units_Sold", "mean")
)

# Combine summaries
summary = inventory_summary.merge(
    sales_summary,
    on="Warehouse_ID"
)

# KPI cards
col1, col2, col3 = st.columns(3)

col1.metric("Total Warehouses", summary["Warehouse_ID"].nunique())

col2.metric(
    "Total Inventory",
    f"{summary['Total_Inventory'].sum():,.0f}"
)

col3.metric(
    "Total Units Sold",
    f"{summary['Total_Units_Sold'].sum():,.0f}"
)

st.divider()

# Inventory comparison
st.subheader("Inventory Comparison by Warehouse")

fig1 = px.bar(
    summary,
    x="Warehouse_ID",
    y="Total_Inventory",
    color="Warehouse_ID",
    title="Total Inventory in Each Warehouse"
)

st.plotly_chart(fig1, width="stretch")

# Sales comparison
st.subheader("Sales Comparison by Warehouse")

fig2 = px.bar(
    summary,
    x="Warehouse_ID",
    y="Total_Units_Sold",
    color="Warehouse_ID",
    title="Total Units Sold by Warehouse"
)

st.plotly_chart(fig2, width="stretch")

# Average inventory
st.subheader("Average Inventory Levels")

fig3 = px.bar(
    summary,
    x="Warehouse_ID",
    y="Average_Inventory",
    color="Warehouse_ID",
    title="Average Inventory per Product"
)

st.plotly_chart(fig3, width="stretch")

# Detailed table
st.subheader("Warehouse Performance Details")

st.dataframe(summary, width="stretch")

# Warehouse filter
st.subheader("Individual Warehouse Details")

selected_warehouse = st.selectbox(
    "Select Warehouse",
    sorted(df["Warehouse_ID"].unique())
)

warehouse_data = df[
    df["Warehouse_ID"] == selected_warehouse
]

daily_sales = warehouse_data.groupby(
    "Date", as_index=False
)["Units_Sold"].sum()

fig4 = px.line(
    daily_sales,
    x="Date",
    y="Units_Sold",
    title=f"Daily Sales Trend - {selected_warehouse}"
)

st.plotly_chart(fig4, width="stretch")
