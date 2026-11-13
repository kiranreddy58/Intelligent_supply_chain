
import streamlit as st

st.set_page_config(
    page_title="About Project",
    page_icon="📘",
    layout="wide"
)

st.title("📘 About the Project")

st.markdown("""
# Intelligent Supply Chain and Inventory Management System

An intelligent dashboard that uses data analytics and
machine learning to support inventory monitoring,
demand prediction and supply chain decision-making.
""")

st.divider()

# PROJECT OBJECTIVES

st.header("🎯 Project Objectives")

st.markdown("""
1. Monitor inventory levels across multiple warehouses.
2. Predict product demand using machine learning.
3. Identify products that require inventory replenishment.
4. Analyze warehouse inventory and sales performance.
5. Study supplier lead times and ordering patterns.
6. Support better inventory management decisions.
""")

st.divider()

# TECHNOLOGIES USED

st.header("🛠️ Technologies Used")

technologies = {
    "Python": "Main programming language used for development.",
    "Streamlit": "Used to build the interactive web dashboard.",
    "Pandas": "Used for dataset loading, cleaning and analysis.",
    "NumPy": "Used for numerical operations.",
    "Plotly": "Used to create interactive charts and graphs.",
    "Scikit-learn": "Used to build and evaluate the demand prediction model.",
    "Joblib": "Available for saving and loading trained machine learning models."
}

for technology, description in technologies.items():
    st.markdown(f"**{technology}:** {description}")

st.divider()

# MACHINE LEARNING

st.header("🤖 Machine Learning Methodology")

st.subheader("Random Forest Regressor")

st.write("""
Random Forest Regressor is used for demand prediction.

It combines multiple decision trees and averages their
predictions to estimate future product demand.
""")

st.markdown("""
**Demand prediction features:**
- Previous day demand (Lag 1)
- Previous 7-day demand (Lag 7)
- Previous 14-day demand (Lag 14)
- Previous 30-day demand (Lag 30)
- Rolling average demand
- Day of the week
- Month
""")

st.subheader("Model Evaluation")

st.markdown("""
- **MAE:** Mean Absolute Error measures the average absolute difference between actual and predicted demand.
- **RMSE:** Root Mean Squared Error gives more weight to larger prediction errors.

Lower values generally indicate better prediction accuracy.
""")

st.divider()

# INVENTORY MANAGEMENT

st.header("📦 Inventory Management")

st.write("""
The system compares current inventory with the reorder point
to identify products that may require replenishment.
""")

st.latex(
    r"ROP = (Average\\ Daily\\ Demand \\times Lead\\ Time) + Safety\\ Stock"
)

st.write("""
ROP means Reorder Point. It represents the inventory level
at which replenishment should be considered.
""")

st.divider()

# DATASET INFORMATION

st.header("📊 Dataset Information")

st.markdown("""
The project uses the High-Dimensional Supply Chain
Inventory Dataset.

**Dataset characteristics:**
- 91,250 records
- 15 columns
- 50 unique SKUs
- 5 warehouses
- 10 suppliers
- 4 regions
- Data period: January to December 2024
""")

st.info(
    "The dataset contains historical supply chain records. "
    "It is synthetic operational data and should not be treated "
    "as live business information."
)

st.divider()

# PROJECT LIMITATIONS

st.header("⚠️ Project Limitations")

st.markdown("""
1. The dataset contains synthetic operational records rather than live business data.
2. Demand predictions depend on the quality and patterns of historical data.
3. The dataset does not provide actual transportation distances.
4. Actual shipping costs and delivery durations are not available.
5. The Stockout_Flag column contains zero recorded stockout events.
6. Supplier analysis is limited to the available lead-time and ordering information.
""")

st.divider()

# FUTURE ENHANCEMENTS

st.header("🚀 Future Enhancements")

st.markdown("""
1. Integrate real-time inventory data using IoT sensors.
2. Connect the system to live supplier and warehouse databases.
3. Add transportation route optimization.
4. Estimate delivery costs and arrival times using logistics data.
5. Improve demand forecasting using advanced machine learning models.
6. Add user authentication and role-based access.
""")

st.divider()

# CONCLUSION

st.header("✅ Project Conclusion")

st.write("""
The Intelligent Supply Chain and Inventory Management System
provides an integrated platform for inventory monitoring,
demand prediction, warehouse analysis and supplier evaluation.

It demonstrates how data analytics and machine learning
can support better supply chain decisions.
""")

st.caption(
    "Intelligent Supply Chain and Inventory Management System"
)
