
# Intelligent Supply Chain and Inventory Management System

## 1. Project Overview

The Intelligent Supply Chain and Inventory Management System is a Python-based web application developed using Streamlit, Data Analytics and Machine Learning.

It helps monitor inventory, predict product demand, analyze warehouse performance and generate inventory replenishment recommendations.

## 2. Project Objectives

- Monitor inventory levels across warehouses.
- Predict future product demand using Machine Learning.
- Identify products requiring replenishment.
- Analyze warehouse performance.
- Evaluate supplier lead times.
- Support better inventory management decisions.

## 3. Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Scikit-learn
- Joblib

## 4. Dataset Information

Dataset: High-Dimensional Supply Chain Inventory Dataset

- Total Records: 91,250
- Total Columns: 15
- Products: 50 SKUs
- Warehouses: 5
- Suppliers: 10
- Regions: 4
- Data Period: January–December 2024

## 5. Dashboard Modules

1. Main Dashboard
2. Inventory Management
3. Demand Prediction
4. Warehouse Analysis
5. Transportation Analysis
6. Inventory Recommendations
7. About Project

## 6. Machine Learning

Random Forest Regressor is used for demand prediction.

Model evaluation metrics:
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)

## 7. Installation and Execution

### Step 1: Clone or download the project

Open the project folder in VS Code.

### Step 2: Create a virtual environment

```bash
python -m venv venv
```

### Step 3: Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Mac/Linux:

```bash
source venv/bin/activate
```

### Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run the application

```bash
streamlit run app.py
```

The dashboard will open in your browser.

## 8. Project Limitations

- The dataset contains synthetic operational records.
- Demand predictions depend on historical data.
- Actual transportation distances and shipping costs are unavailable.
- The dataset contains zero recorded stockout events.

## 9. Future Enhancements

- Real-time inventory monitoring.
- IoT integration.
- Transportation route optimization.
- Advanced demand forecasting.
- Live supplier database integration.
- User authentication.

## 10. Conclusion

This project demonstrates how data analytics and machine learning can support inventory management, demand forecasting and supply chain decision-making.
