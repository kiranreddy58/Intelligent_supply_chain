
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🚚 Transportation and Supplier Analysis")

@st.cache_data
def load_data():
    df = pd.read_csv("data/raw/supply_chain_dataset1.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# Supplier performance summary
supplier_summary = df.groupby(
    "Supplier_ID", as_index=False
).agg(
    Average_Lead_Time=("Supplier_Lead_Time_Days", "mean"),
    Total_Order_Quantity=("Order_Quantity", "sum"),
    Average_Order_Quantity=("Order_Quantity", "mean"),
    Total_Units_Sold=("Units_Sold", "sum")
)

# KPI metrics
col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Suppliers",
    df["Supplier_ID"].nunique()
)

col2.metric(
    "Average Lead Time",
    f"{df['Supplier_Lead_Time_Days'].mean():.2f} days"
)

col3.metric(
    "Total Order Quantity",
    f"{df['Order_Quantity'].sum():,.0f}"
)

st.divider()

# Supplier lead time
st.subheader("Supplier Lead Time Comparison")

fig1 = px.bar(
    supplier_summary,
    x="Supplier_ID",
    y="Average_Lead_Time",
    color="Supplier_ID",
    title="Average Delivery Lead Time by Supplier"
)

st.plotly_chart(fig1, width="stretch")

# Order quantity
st.subheader("Supplier Order Quantity")

fig2 = px.bar(
    supplier_summary,
    x="Supplier_ID",
    y="Total_Order_Quantity",
    color="Supplier_ID",
    title="Total Order Quantity by Supplier"
)

st.plotly_chart(fig2, width="stretch")

# Lead time distribution
st.subheader("Lead Time Distribution")

fig3 = px.histogram(
    df,
    x="Supplier_Lead_Time_Days",
    nbins=20,
    title="Distribution of Supplier Lead Times"
)

st.plotly_chart(fig3, width="stretch")

# Supplier table
st.subheader("Supplier Performance Details")

st.dataframe(
    supplier_summary.sort_values(
        "Average_Lead_Time"
    ),
    width="stretch"
)

# Supplier filter
st.subheader("Individual Supplier Analysis")

selected_supplier = st.selectbox(
    "Select Supplier",
    sorted(df["Supplier_ID"].unique())
)

supplier_data = df[
    df["Supplier_ID"] == selected_supplier
]

st.write(
    f"Average lead time: "
    f"{supplier_data['Supplier_Lead_Time_Days'].mean():.2f} days"
)

st.write(
    f"Total orders: "
    f"{supplier_data['Order_Quantity'].sum():,.0f}"
)

