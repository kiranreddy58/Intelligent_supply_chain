
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("💡 Intelligent Inventory Recommendations")

@st.cache_data
def load_data():
    df = pd.read_csv("data/raw/supply_chain_dataset1.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# Latest inventory snapshot
latest_date = df["Date"].max()

latest = df[df["Date"] == latest_date].copy()

# Calculate average daily demand for each SKU and warehouse
demand = df.groupby(
    ["SKU_ID", "Warehouse_ID"],
    as_index=False
).agg(
    Average_Daily_Demand=("Units_Sold", "mean")
)

# Merge demand information
latest = latest.merge(
    demand,
    on=["SKU_ID", "Warehouse_ID"],
    how="left"
)

# Calculate lead-time demand
latest["Lead_Time_Demand"] = (
    latest["Average_Daily_Demand"]
    * latest["Supplier_Lead_Time_Days"]
)

# Calculate recommended order quantity
latest["Recommended_Order"] = (
    latest["Reorder_Point"] - latest["Inventory_Level"]
).clip(lower=0)

# Calculate priority
def get_priority(row):
    if row["Inventory_Level"] <= row["Lead_Time_Demand"]:
        return "High"
    elif row["Inventory_Level"] <= row["Reorder_Point"]:
        return "Medium"
    else:
        return "Low"

latest["Priority"] = latest.apply(get_priority, axis=1)

# Recommendation
def get_recommendation(row):
    if row["Priority"] == "High":
        return "Urgent stock review required"
    elif row["Priority"] == "Medium":
        return "Place replenishment order"
    else:
        return "Stock level is sufficient"

latest["Recommendation"] = latest.apply(
    get_recommendation,
    axis=1
)

# KPI metrics
high = (latest["Priority"] == "High").sum()
medium = (latest["Priority"] == "Medium").sum()
low = (latest["Priority"] == "Low").sum()

col1, col2, col3 = st.columns(3)

col1.metric("High Priority", high)
col2.metric("Medium Priority", medium)
col3.metric("Low Priority", low)

st.divider()

# Filter recommendations
st.subheader("Inventory Recommendation Details")

priority_filter = st.selectbox(
    "Filter by Priority",
    ["All", "High", "Medium", "Low"]
)

if priority_filter == "All":
    filtered = latest.copy()
else:
    filtered = latest[
        latest["Priority"] == priority_filter
    ]

st.dataframe(
    filtered[
        [
            "SKU_ID",
            "Warehouse_ID",
            "Supplier_ID",
            "Inventory_Level",
            "Reorder_Point",
            "Average_Daily_Demand",
            "Lead_Time_Demand",
            "Recommended_Order",
            "Priority",
            "Recommendation"
        ]
    ],
    width="stretch"
)

# Priority distribution
st.subheader("Priority Distribution")

priority_data = latest["Priority"].value_counts().reset_index()
priority_data.columns = ["Priority", "Count"]

fig1 = px.pie(
    priority_data,
    names="Priority",
    values="Count",
    title="Inventory Priority Distribution"
)

st.plotly_chart(fig1, width="stretch")

# Recommended order chart
st.subheader("Recommended Order Quantity")

reorder_data = latest[
    latest["Recommended_Order"] > 0
]

if not reorder_data.empty:
    fig2 = px.bar(
        reorder_data,
        x="SKU_ID",
        y="Recommended_Order",
        color="Warehouse_ID",
        title="Recommended Order Quantity by Product"
    )

    st.plotly_chart(fig2, width="stretch")
else:
    st.info("No products currently require reordering.")

# Download recommendations
st.subheader("Download Recommendations")

csv = latest.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Recommendation Report",
    data=csv,
    file_name="inventory_recommendations.csv",
    mime="text/csv"
)
