import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="RetailPulse | Retail Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# 2. DASHBOARD STYLING
# --------------------------------------------------

st.markdown("""
<style>
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }

    [data-testid="stMetric"] {
        background-color: #1e293b;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #334155;
    }

    h1, h2, h3 {
        color: #5eead4;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 3. LOAD DATASET
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("retailpulse_cleaned.csv")

    df.columns = df.columns.str.strip()

    # Standardize common column names
    rename_map = {
        "Customer ID": "Customer ID",
        "Customer ID ": "Customer ID",
        "InvoiceDate": "InvoiceDate",
        "Price": "Price",
        "Quantity": "Quantity"
    }

    df = df.rename(columns=rename_map)

    if "Quantity" in df.columns and "Price" in df.columns:
        df["TotalSales"] = df["Quantity"] * df["Price"]

    if "Customer ID" in df.columns:
        df["Customer ID"] = pd.to_numeric(
            df["Customer ID"], errors="coerce"
        )

    return df


try:
    df = load_data()
    data_loaded = True
    load_error = None
except Exception as e:
    df = pd.DataFrame()
    data_loaded = False
    load_error = str(e)

# --------------------------------------------------
# 4. SIDEBAR NAVIGATION
# --------------------------------------------------

st.sidebar.title("📊 RetailPulse")
st.sidebar.caption("AI-Powered Retail Intelligence")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Sales Analytics",
        "Customer Segmentation",
        "Demand Forecasting",
        "Churn Analysis",
        "Inventory Optimization",
        "Model Monitoring"
    ]
)

st.sidebar.divider()
st.sidebar.caption("RetailPulse | Project Dashboard")

# --------------------------------------------------
# 5. DASHBOARD HEADER
# --------------------------------------------------

st.title("RetailPulse")
st.write(
    "AI-Powered Customer Analytics & Demand Forecasting Platform"
)
st.divider()

# --------------------------------------------------
# 6. OVERVIEW PAGE
# --------------------------------------------------

if page == "Overview":
    st.subheader("Business Overview")

    if data_loaded:
        # Calculate actual dataset metrics
        if "Customer ID" in df.columns:
            total_customers = int(df["Customer ID"].nunique())
        else:
            total_customers = 0

        if "TotalSales" in df.columns:
            if "Quantity" in df.columns:
                valid_sales = df.loc[df["Quantity"] > 0, "TotalSales"]
                total_sales = valid_sales.sum()
            else:
                total_sales = df["TotalSales"].sum()
        else:
            total_sales = 0

        if "Invoice" in df.columns:
            total_orders = int(df["Invoice"].nunique())
        else:
            total_orders = 0

        # KPI cards
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Customers", f"{total_customers:,}")
        col2.metric("Total Revenue", f"£{total_sales:,.2f}")
        col3.metric("Total Orders", f"{total_orders:,}")
        col4.metric("Dataset Rows", f"{len(df):,}")

        st.subheader("Dataset Preview")
        st.dataframe(df.head(10), use_container_width=True)

        st.subheader("Project Modules")

        modules = pd.DataFrame({
            "Module": [
                "Sales Analytics",
                "Customer Segmentation",
                "Demand Forecasting",
                "Churn Analysis",
                "Inventory Optimization",
                "Model Monitoring"
            ],
            "Status": [
                "Dashboard development",
                "Dashboard development",
                "Dashboard development",
                "Dashboard development",
                "Dashboard development",
                "Dashboard development"
            ]
        })

        st.dataframe(
            modules,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.error("Dataset could not be loaded.")
        st.code(load_error)
        st.info(
            "Check that online_retail_II.xlsx is in the RetailPulse folder."
        )

# --------------------------------------------------
# 7. SALES ANALYTICS PAGE
# --------------------------------------------------

elif page == "Sales Analytics":
    st.subheader("Sales Analytics")

    if data_loaded and "TotalSales" in df.columns:

        # Total sales metric
        total_sales = df["TotalSales"].sum()
        st.metric("Total Sales Value", f"£{total_sales:,.2f}")

        # ------------------------------------------
        # MONTHLY SALES TREND
        # ------------------------------------------
        st.subheader("Monthly Sales Trend")

        if "InvoiceDate" in df.columns:
            sales_df = df.copy()

            sales_df["InvoiceDate"] = pd.to_datetime(
                sales_df["InvoiceDate"], errors="coerce"
            )

            sales_df = sales_df.dropna(subset=["InvoiceDate"])

            monthly_sales = (
                sales_df.set_index("InvoiceDate")
                .resample("MS")["TotalSales"]
                .sum()
                .reset_index()
            )

            monthly_sales["Month"] = (
                monthly_sales["InvoiceDate"].dt.strftime("%b %Y")
            )

            fig_trend = px.line(
                monthly_sales,
                x="Month",
                y="TotalSales",
                markers=True,
                title="Monthly Revenue Trend",
                template="plotly_dark"
            )

            fig_trend.update_layout(
                xaxis_title="Month",
                yaxis_title="Total Sales (£)",
                xaxis_tickangle=-45
            )

            st.plotly_chart(
                fig_trend, use_container_width=True
            )

            st.subheader("Monthly Sales Data")
            st.dataframe(
                monthly_sales[["Month", "TotalSales"]],
                use_container_width=True
            )

        else:
            st.warning(
                "InvoiceDate column was not found in the dataset."
            )

        # ------------------------------------------
        # TOP 10 COUNTRIES BY SALES
        # ------------------------------------------
        st.subheader("Top 10 Countries by Sales")

        if "Country" in df.columns:
            country_sales = (
                df.groupby("Country", as_index=False)["TotalSales"]
                .sum()
                .sort_values("TotalSales", ascending=False)
                .head(10)
            )

            fig_country = px.bar(
                country_sales,
                x="Country",
                y="TotalSales",
                title="Top 10 Countries by Sales",
                template="plotly_dark"
            )

            st.plotly_chart(
                fig_country, use_container_width=True
            )

        else:
            st.info("Country column was not found in the dataset.")

    else:
        st.warning(
            "Sales data is unavailable. Check dataset loading."
        )

# --------------------------------------------------
# 8. CUSTOMER SEGMENTATION PAGE
# --------------------------------------------------

elif page == "Customer Segmentation":
    st.subheader("Customer Segmentation")

    try:
        rfm = pd.read_csv("retailpulse_rfm.csv")
        clusters = pd.read_csv("retailpulse_clusters.csv")
        summary = pd.read_csv("retailpulse_cluster_summary.csv")

        col1, col2 = st.columns(2)
        col1.metric("Customers Analyzed", f"{rfm.shape[0]:,}")
        col2.metric("Number of Clusters", "5")

        st.subheader("Customer Segment Distribution")
        if "Segment" in rfm.columns:
            segment_counts = (
                rfm["Segment"].value_counts().reset_index()
            )
            segment_counts.columns = ["Segment", "Customers"]
            fig = px.bar(
                segment_counts,
                x="Segment",
                y="Customers",
                title="Customers by RFM Segment",
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("RFM Customer Data")
        st.dataframe(rfm.head(20), use_container_width=True)

        st.subheader("K-Means Cluster Summary")
        st.dataframe(summary, use_container_width=True)

    except Exception as e:
        st.error("Could not load segmentation files.")
        st.code(str(e))
    



# =========================
# DEMAND FORECASTING
# =========================

elif page == "Demand Forecasting":
    st.title("📈 Demand Forecasting")
    st.write(
        "Analyze predicted demand, compare forecasting models, "
        "and simulate changes in expected demand."
    )

    try:
        # Load forecast data
        forecast_df = pd.read_csv("data/forecast_results.csv")

        # Required forecast columns:
        # Prophet, LSTM, Hybrid
        required_columns = ["Prophet", "LSTM", "Hybrid"]

        missing_columns = [
            col for col in required_columns
            if col not in forecast_df.columns
        ]

        if missing_columns:
            st.error(
                f"Missing forecast columns: {missing_columns}"
            )
            st.stop()

        # Convert forecast values to numeric
        for col in required_columns:
            forecast_df[col] = pd.to_numeric(
                forecast_df[col],
                errors="coerce"
            )

        forecast_df = forecast_df.dropna(
            subset=required_columns
        ).reset_index(drop=True)

        if forecast_df.empty:
            st.warning("No valid forecast data is available.")
            st.stop()

        # -------------------------
        # Forecast summary metrics
        # -------------------------
        st.subheader("Forecast Summary")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Prophet Average",
                f"{forecast_df['Prophet'].mean():,.2f}"
            )

        with col2:
            st.metric(
                "LSTM Average",
                f"{forecast_df['LSTM'].mean():,.2f}"
            )

        with col3:
            st.metric(
                "Hybrid Average",
                f"{forecast_df['Hybrid'].mean():,.2f}"
            )

        # -------------------------
        # Forecast comparison
        # -------------------------
        st.subheader("Forecast Comparison")

        comparison_df = forecast_df[
            ["Prophet", "LSTM", "Hybrid"]
        ].copy()

        comparison_df["Observation"] = range(
            1, len(comparison_df) + 1
        )

        fig_comparison = px.line(
            comparison_df,
            x="Observation",
            y=["Prophet", "LSTM", "Hybrid"],
            title="Prophet vs LSTM vs Hybrid Forecast",
            template="plotly_dark"
        )

        st.plotly_chart(
            fig_comparison,
            use_container_width=True,
            key="forecast_comparison_chart"
        )

        # -------------------------
        # Model evaluation metrics
        # -------------------------
        st.subheader("Model Evaluation")

        # If actual values are available, calculate MAE and RMSE.
        actual_column = "Actual"

        if actual_column in forecast_df.columns:
            actual = pd.to_numeric(
                forecast_df[actual_column],
                errors="coerce"
            )

            valid = actual.notna()

            if valid.any():
                metric_cols = st.columns(3)

                for idx, model in enumerate(
                    ["Prophet", "LSTM", "Hybrid"]
                ):
                    predicted = forecast_df.loc[
                        valid, model
                    ]
                    actual_valid = actual.loc[valid]

                    mae = mean_absolute_error(
                        actual_valid, predicted
                    )
                    rmse = np.sqrt(
                        mean_squared_error(
                            actual_valid, predicted
                        )
                    )

                    with metric_cols[idx]:
                        st.write(f"**{model}**")
                        st.metric("MAE", f"{mae:,.2f}")
                        st.metric("RMSE", f"{rmse:,.2f}")
            else:
                st.info(
                    "Actual values are unavailable for model evaluation."
                )
        else:
            st.info(
                "Add an 'Actual' column to calculate MAE and RMSE."
            )

        # -------------------------
        # Demand change alerts
        # -------------------------
        st.subheader("Demand Change Alerts")

        hybrid = forecast_df["Hybrid"]

        if len(hybrid) >= 2:
            first_value = float(hybrid.iloc[0])
            last_value = float(hybrid.iloc[-1])

            if first_value != 0:
                change_pct = (
                    (last_value - first_value)
                    / abs(first_value)
                ) * 100
            else:
                change_pct = 0.0

            if change_pct >= 10:
                st.success(
                    f"📈 Forecast demand increases by "
                    f"{change_pct:.2f}% across the forecast period."
                )
            elif change_pct <= -10:
                st.warning(
                    f"📉 Forecast demand decreases by "
                    f"{abs(change_pct):.2f}% across the forecast period."
                )
            else:
                st.info(
                    f"Forecast demand is relatively stable "
                    f"({change_pct:.2f}% change)."
                )

        # -------------------------
        # What-if demand analysis
        # -------------------------
        st.subheader("What-if Demand Analysis")

        st.write(
            "Adjust expected demand to simulate an alternative scenario."
        )

        demand_change = st.slider(
            "Expected demand change (%)",
            min_value=-30,
            max_value=30,
            value=0,
            step=5,
            key="what_if_demand_change"
        )

        what_if_df = pd.DataFrame({
            "Observation": range(
                1, len(forecast_df) + 1
            ),
            "Hybrid Forecast": forecast_df[
                "Hybrid"
            ].to_numpy()
        })

        what_if_df["What-if Forecast"] = (
            what_if_df["Hybrid Forecast"]
            * (1 + demand_change / 100)
        )

        fig_whatif = px.line(
            what_if_df,
            x="Observation",
            y="Hybrid Forecast",
            title="Hybrid Forecast vs What-if Scenario",
            template="plotly_dark"
        )

        fig_whatif.add_scatter(
            x=what_if_df["Observation"],
            y=what_if_df["What-if Forecast"],
            mode="lines",
            name="What-if Forecast"
        )

        st.plotly_chart(
            fig_whatif,
            use_container_width=True,
            key="what_if_forecast_chart"
        )

        st.metric(
            "Adjusted Average Forecast",
            f"{what_if_df['What-if Forecast'].mean():,.2f}"
        )

        # -------------------------
        # Forecast data tables
        # -------------------------
        st.subheader("Forecast Data")

        st.dataframe(
            forecast_df,
            use_container_width=True
        )

        st.subheader("What-if Scenario Data")

        st.dataframe(
            what_if_df,
            use_container_width=True
        )

    except FileNotFoundError as e:
        st.error(
            "Forecast data file was not found. "
            "Check the CSV file path in your project."
        )
        st.code(str(e))

    except Exception as e:
        st.error("Could not load forecasting data.")
        st.code(str(e))

# --------------------------------------------------
# 10. CHURN ANALYSIS PAGE
# --------------------------------------------------

elif page == "Churn Analysis":
    st.subheader("Churn Analysis")

    try:
        churn_df = pd.read_csv("retailpulse_churn_results.csv")
        summary_df = pd.read_csv("retailpulse_churn_summary.csv")
        importance_df = pd.read_csv(
            "retailpulse_feature_importance.csv"
        )

        # Calculate customer metrics
        total = int(summary_df["Customers"].sum())

        churned = int(
            summary_df.loc[
                summary_df["Churn_Status"] == "Churned",
                "Customers"
            ].sum()
        )

        not_churned = total - churned

        churn_rate = (
            (churned / total * 100) if total > 0 else 0
        )

        # Customer metrics
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Customers", f"{total:,}")
        col2.metric("Churned Customers", f"{churned:,}")
        col3.metric("Churn Rate", f"{churn_rate:.2f}%")

        # Customer risk alerts
        st.subheader("Customer Risk Alerts")

        if churn_rate >= 30:
            st.error(
                f"🔴 High Churn Risk: {churn_rate:.2f}% of customers "
                "are marked as churned. Review customer retention "
                "actions."
            )
        elif churn_rate >= 15:
            st.warning(
                f"🟠 Moderate Churn Risk: {churn_rate:.2f}%. "
                "Monitor customer retention."
            )
        else:
            st.success(
                f"🟢 Churn rate is {churn_rate:.2f}%. "
                "No high-churn alert triggered."
            )

        # Churn distribution chart
        st.subheader("Churn Distribution")

        fig = px.pie(
            summary_df,
            names="Churn_Status",
            values="Customers",
            title="Churned vs Not Churned",
            template="plotly_dark"
        )

        st.plotly_chart(fig, use_container_width=True)

        # Model evaluation
        st.subheader("Model Evaluation")

        accuracy = (
            churn_df["Actual_Churn"]
            == churn_df["Predicted_Churn"]
        ).mean()

        st.metric("Test Accuracy", f"{accuracy:.2%}")

        # Feature importance chart
        st.subheader("Feature Importance")

        importance_df = importance_df.sort_values(
            "Importance",
            ascending=False
        )

        fig2 = px.bar(
            importance_df,
            x="Importance",
            y=importance_df.index,
            orientation="h",
            title="Feature Importance",
            template="plotly_dark"
        )

        st.plotly_chart(fig2, use_container_width=True)

        # Customer count summary
        st.subheader("Customer Summary")

        st.write(f"Not Churned Customers: {not_churned:,}")
        st.write(f"Churned Customers: {churned:,}")

    except Exception as e:
        st.error("Could not load churn analysis files.")
        st.code(str(e))


# --------------------------------------------------
# 11. INVENTORY OPTIMIZATION PAGE
# -------------------------------------------------

elif page == "Inventory Optimization":
    st.subheader("Inventory Optimization")

    try:
        inventory_df = pd.read_csv(
            "retailpulse_inventory_summary.csv"
        )

        values = inventory_df.set_index("Metric")["Value"]

        # Inventory metrics
        col1, col2 = st.columns(2)

        col1.metric(
            "Average Demand",
            f"{float(values['Average Demand']):,.2f}"
        )

        col2.metric(
            "Demand Standard Deviation",
            f"{float(values['Demand Standard Deviation']):,.2f}"
        )

        col3, col4, col5 = st.columns(3)

        col3.metric(
            "Safety Stock",
            f"{float(values['Safety Stock']):,.2f}"
        )

        col4.metric(
            "Reorder Point",
            f"{float(values['Reorder Point']):,.2f}"
        )

        col5.metric(
            "Recommended Target Inventory",
            f"{float(values['Recommended Target Inventory']):,.2f}"
        )

        # Inventory risk alert
        st.subheader("Inventory Risk Alerts")

        safety_stock = float(values["Safety Stock"])
        reorder_point = float(values["Reorder Point"])
        target_inventory = float(
            values["Recommended Target Inventory"]
        )

        if target_inventory < reorder_point:
            st.error(
                "High Inventory Risk: Recommended target inventory "
                "is below the reorder point. Review replenishment."
            )
        elif safety_stock > 0 and reorder_point > 0:
            st.warning(
                "Inventory Planning Alert: Monitor stock levels "
                "against the reorder point and safety stock."
            )
        else:
            st.info(
                "Check inventory inputs before assessing inventory risk."
            )

        # Inventory summary table
        st.subheader("Inventory Summary")

        st.dataframe(
            inventory_df,
            use_container_width=True
        )

        # Inventory metrics graph
        st.subheader("Inventory Metrics Overview")

        chart_df = inventory_df.copy()

        fig_inventory = px.bar(
            chart_df,
            x="Metric",
            y="Value",
            text="Value",
            title="Inventory Planning Metrics",
            template="plotly_dark"
        )

        fig_inventory.update_layout(
            xaxis_title="Inventory Metric",
            yaxis_title="Value"
        )

        st.plotly_chart(
            fig_inventory,
            use_container_width=True
        )

    except Exception as e:
        st.error("Could not load inventory optimization files.")
        st.code(str(e))


# --------------------------------------------------
# 12. MODEL MONITORING PAGE
# --------------------------------------------------
elif page == "Model Monitoring":
    st.subheader("Model Monitoring")

    try:
        monitoring_df = pd.read_csv(
            "retailpulse_monitoring_summary.csv"
        )

        # Read monitoring values
        values = monitoring_df.set_index("Metric")["Value"]

        # First row of metrics
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Reference Rows",
            f"{int(values['Reference Rows']):,}"
        )

        col2.metric(
            "Current Rows",
            f"{int(values['Current Rows']):,}"
        )

        col3.metric(
            "Features Monitored",
            f"{int(values['Features Monitored']):,}"
        )

        # Second row of metrics
        col4, col5 = st.columns(2)

        col4.metric(
            "Drifted Columns",
            f"{int(values['Drifted Columns']):,}"
        )

        col5.metric(
            "Drift Share",
            f"{float(values['Drift Share']):.1%}"
        )

        # Monitoring summary table
        st.subheader("Monitoring Summary")
        st.dataframe(
            monitoring_df,
            use_container_width=True
        )

        # Monitoring metrics graph
        st.subheader("Model Monitoring Metrics")

        drift_data = pd.DataFrame({
            "Metric": [
                "Reference Rows",
                "Current Rows",
                "Features Monitored",
                "Drifted Columns"
            ],
            "Value": [
                int(values["Reference Rows"]),
                int(values["Current Rows"]),
                int(values["Features Monitored"]),
                int(values["Drifted Columns"])
            ]
        })

        fig_drift = px.bar(
            drift_data,
            x="Metric",
            y="Value",
            text="Value",
            title="Model Monitoring Overview",
            template="plotly_dark"
        )

        fig_drift.update_layout(
            xaxis_title="Monitoring Metric",
            yaxis_title="Count"
        )

        st.plotly_chart(
            fig_drift,
            use_container_width=True
        )

        # Drift status message
        drifted_count = int(values["Drifted Columns"])

        if drifted_count > 0:
            st.warning(
                f"{drifted_count} feature(s) show drift. "
                "Further investigation is recommended."
            )
        else:
            st.success(
                "No feature drift detected in the current "
                "monitoring summary."
            )

    except Exception as e:
        st.error("Could not load monitoring summary.")
        st.code(str(e))
