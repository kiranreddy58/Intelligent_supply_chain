
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📦 Inventory Management")

@st.cache_data
def load_data():
    df = pd.read_csv("data/raw/supply_chain_dataset1.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# Get the latest inventory records
latest_date = df["Date"].max()
latest = df[df["Date"] == latest_date].copy()

# Calculate inventory status
latest["Status"] = latest.apply(
    lambda row: "Reorder Required"
    if row["Inventory_Level"] <= row["Reorder_Point"]
    else "Sufficient Stock",
    axis=1
)

latest["Recommended_Order"] = (
    latest["Reorder_Point"] - latest["Inventory_Level"]
).clip(lower=0)

# KPI calculations
total_inventory = latest["Inventory_Level"].sum()

reorder_count = (
    latest["Status"] == "Reorder Required"
).sum()

inventory_value = (
    latest["Inventory_Level"] * latest["Unit_Cost"]
).sum()

col1, col2, col3 = st.columns(3)

col1.metric("Total Inventory Units", f"{total_inventory:,.0f}")
col2.metric("Products Below Reorder Point", reorder_count)
col3.metric("Inventory Value", f"₹{inventory_value:,.2f}")

st.divider()

# Warehouse filter
st.subheader("Inventory Details")

warehouses = ["All Warehouses"] + sorted(
    latest["Warehouse_ID"].unique().tolist()
)

selected = st.selectbox("Select Warehouse", warehouses)

if selected != "All Warehouses":
    filtered = latest[latest["Warehouse_ID"] == selected]
else:
    filtered = latest

st.dataframe(
    filtered[
        [
            "SKU_ID",
            "Warehouse_ID",
            "Inventory_Level",
            "Reorder_Point",
            "Recommended_Order",
            "Status"
        ]
    ],
    width="stretch"
)

# Reorder recommendations
st.subheader("Reorder Recommendations")

reorder_data = filtered[
    filtered["Recommended_Order"] > 0
]

if not reorder_data.empty:
    st.dataframe(
        reorder_data[
            [
                "SKU_ID",
                "Warehouse_ID",
                "Inventory_Level",
                "Reorder_Point",
                "Recommended_Order"
            ]
        ],
        width="stretch"
    )
else:
    st.success("No products require reordering in this selection.")

# Warehouse chart
st.subheader("Inventory by Warehouse")

warehouse_data = latest.groupby(
    "Warehouse_ID", as_index=False
)["Inventory_Level"].sum()

fig = px.bar(
    warehouse_data,
    x="Warehouse_ID",
    y="Inventory_Level",
    color="Warehouse_ID",
    title="Current Inventory Across Warehouses"
)

st.plotly_chart(fig, width="stretch")
