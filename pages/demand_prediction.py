
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

st.title("🤖 AI-Based Demand Prediction")

@st.cache_data
def load_data():
    df = pd.read_csv("data/raw/supply_chain_dataset1.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

st.write("Predict future product demand using Random Forest Regression.")

# Select product
sku_list = sorted(df["SKU_ID"].unique())

selected_sku = st.selectbox("Select Product (SKU)", sku_list)

# Prepare daily demand data
product_data = (
    df[df["SKU_ID"] == selected_sku]
    .groupby("Date")["Units_Sold"]
    .sum()
    .sort_index()
    .asfreq("D", fill_value=0)
)

# Create time-based features
model_data = pd.DataFrame(index=product_data.index)
model_data["Demand"] = product_data

for lag in [1, 7, 14, 30]:
    model_data[f"Lag_{lag}"] = model_data["Demand"].shift(lag)

model_data["Rolling_7"] = (
    model_data["Demand"].shift(1).rolling(7).mean()
)

model_data["Rolling_30"] = (
    model_data["Demand"].shift(1).rolling(30).mean()
)

model_data["Day_Of_Week"] = model_data.index.dayofweek
model_data["Month"] = model_data.index.month

model_data = model_data.dropna()

features = [
    "Lag_1", "Lag_7", "Lag_14", "Lag_30",
    "Rolling_7", "Rolling_30",
    "Day_Of_Week", "Month"
]

X = model_data[features]
y = model_data["Demand"]

# Chronological train-test split
split = int(len(model_data) * 0.8)

X_train = X.iloc[:split]
X_test = X.iloc[split:]

y_train = y.iloc[:split]
y_test = y.iloc[split:]

# Train model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    min_samples_leaf=2,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Evaluate model
predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))

col1, col2 = st.columns(2)

col1.metric("MAE", f"{mae:.2f}")
col2.metric("RMSE", f"{rmse:.2f}")

st.caption("Evaluation uses a chronological 80% training / 20% testing split.")

# Actual vs predicted chart
comparison = pd.DataFrame({
    "Date": y_test.index,
    "Actual Demand": y_test.values,
    "Predicted Demand": predictions
})

st.subheader("Actual vs Predicted Demand")

fig = px.line(
    comparison,
    x="Date",
    y=["Actual Demand", "Predicted Demand"],
    title=f"Demand Prediction for {selected_sku}"
)

st.plotly_chart(fig, width="stretch")

# Future demand forecast
st.subheader("Next 7 Days Demand Forecast")

history = product_data.copy()
future_rows = []

for i in range(7):
    next_date = history.index[-1] + pd.Timedelta(days=1)

    row = pd.DataFrame([{
        "Lag_1": history.iloc[-1],
        "Lag_7": history.iloc[-7],
        "Lag_14": history.iloc[-14],
        "Lag_30": history.iloc[-30],
        "Rolling_7": history.iloc[-7:].mean(),
        "Rolling_30": history.iloc[-30:].mean(),
        "Day_Of_Week": next_date.dayofweek,
        "Month": next_date.month
    }])

    predicted = max(0, model.predict(row[features])[0])

    future_rows.append({
        "Date": next_date,
        "Predicted Demand": round(predicted, 2)
    })

    history.loc[next_date] = predicted

forecast = pd.DataFrame(future_rows)

st.dataframe(forecast, width="stretch")

fig2 = px.bar(
    forecast,
    x="Date",
    y="Predicted Demand",
    title="Forecasted Demand for Next 7 Days"
)

st.plotly_chart(fig2, width="stretch")

# Feature importance
st.subheader("Factors Affecting Demand Prediction")

importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
}).sort_values("Importance", ascending=False)

fig3 = px.bar(
    importance,
    x="Importance",
    y="Feature",
    orientation="h",
    title="Random Forest Feature Importance"
)

st.plotly_chart(fig3, width="stretch")
