
import streamlit as st
import pandas as pd
import plotly.express as px

# Theme Configuration
dark_mode = st.session_state.get("dark_mode", False)

if dark_mode:
    plotly_template = "plotly_dark"
    grid_color = "#344454"
    text_color = "#E2E8F0"
    paper_color = "#1B2732"
    plot_color = "#1B2732"
else:
    plotly_template = "plotly_white"
    grid_color = "#E2E8F0"
    text_color = "#263746"
    paper_color = "#FFFFFF"
    plot_color = "#FFFFFF"


# Page Header
st.title("Predictions")
st.caption(
    "Explore future territorial trends "
    "through predictive analysis."
)

st.divider()

# Prediction Configuration
st.subheader("Prediction Configuration")
st.caption("Configure the parameters for predictive analysis.")

col1, col2 = st.columns(2)

with col1:
    analysis_scope = st.selectbox(
        "Analysis Scope",
        ["Global", "Territorial"]
    )

with col2:
    indicator = st.selectbox(
        "Indicator",
        [
            "Energy Consumption",
            "Population Density",
            "Economic Activity",
            "Renewable Energy Production"
        ]
    )

# Territorial Selection
if analysis_scope == "Global":

    region = st.selectbox(
        "Geographical Scope",
        [
            "Portugal",
            "Centro",
            "Norte",
            "Lisboa e Vale do Tejo",
            "Alentejo",
            "Algarve"
        ]
    )

else:

    territories = st.multiselect(
        "Select Territories",
        [
            "Guarda",
            "Covilhã",
            "Lisboa",
            "Porto",
            "Braga",
            "Aveiro",
            "Coimbra",
            "Viseu"
        ],
        default=["Guarda"]
    )

# Prediction Model
col1, col2 = st.columns(2)

with col1:
    prediction_model = st.selectbox(
        "Prediction Model",
        [
            "Linear Regression",
            "Random Forest Regressor",
            "ARIMA",
            "Exponential Smoothing"
        ]
    )

with col2:
    forecast_horizon = st.selectbox(
        "Forecast Horizon",
        ["1 Year", "3 Years", "5 Years", "10 Years"]
    )

# Historical Period
st.markdown("#### Historical Period")

col1, col2 = st.columns(2)

with col1:
    start_year = st.selectbox(
        "Start Year",
        range(2000, 2027),
        index=0
    )

with col2:
    end_year = st.selectbox(
        "End Year",
        range(2000, 2027),
        index=6
    )

if start_year > end_year:
    st.error("Start year cannot be later than end year.")


st.divider()
st.markdown("#### Model Parameters")

if prediction_model == "Linear Regression":

    col1, col2 = st.columns(2)

    with col1:
        fit_intercept = st.toggle(
            "Fit Intercept",
            value=True
        )

    with col2:
        positive_coefficients = st.toggle(
            "Positive Coefficients Only",
            value=False
        )

elif prediction_model == "Random Forest Regressor":

    col1, col2 = st.columns(2)

    with col1:
        n_estimators = st.slider(
            "Number of Trees",
            min_value=50,
            max_value=500,
            value=100,
            step=50
        )

    with col2:
        max_depth = st.slider(
            "Maximum Tree Depth",
            min_value=2,
            max_value=30,
            value=10
        )

elif prediction_model == "ARIMA":

    col1, col2, col3 = st.columns(3)

    with col1:
        arima_p = st.number_input(
            "AR (p)",
            min_value=0,
            max_value=5,
            value=1
        )

    with col2:
        arima_d = st.number_input(
            "Differencing (d)",
            min_value=0,
            max_value=2,
            value=1
        )

    with col3:
        arima_q = st.number_input(
            "MA (q)",
            min_value=0,
            max_value=5,
            value=1
        )

elif prediction_model == "Exponential Smoothing":

    col1, col2 = st.columns(2)

    with col1:
        trend_component = st.selectbox(
            "Trend Component",
            ["None", "Additive", "Multiplicative"]
        )

    with col2:
        seasonal_component = st.selectbox(
            "Seasonal Component",
            ["None", "Additive", "Multiplicative"]
        )

    st.divider()

col1, col2 = st.columns([3, 1])

with col1:
    st.caption(
        "Generate predictions using the selected model and configuration."
    )

with col2:
    run_prediction = st.button(
        "Run Prediction",
        type="primary",
        use_container_width=True
    )

if run_prediction:
    valid_configuration = True

    if start_year > end_year:
        valid_configuration = False
        st.warning("Invalid historical period.")

    if analysis_scope == "Territorial" and not territories:
        valid_configuration = False
        st.warning("Select at least one territory.")

    if valid_configuration:
        st.info(
            "Configuration validated. "
            "Prediction execution will be connected to the analytics service."
        )


st.divider()
st.subheader("Prediction Overview")
st.caption("Summary of the generated prediction results.")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Expected Change",
        value="+12.4%",
        delta="Compared to last historical year"
    )

with col2:
    st.metric(
        label="Predicted Value",
        value="584.2 MWh"
    )

with col3:
    st.metric(
        label="Model R²",
        value="0.89"
    )

with col4:
    st.metric(
        label="Forecast Until",
        value=str(end_year + int(forecast_horizon.split()[0]))
    )

import numpy as np

# Temporary Mock Forecast Data
historical_data = pd.DataFrame({
    "Year": list(range(2016, 2026)),
    "Value": [
        390, 405, 398, 420, 435,
        428, 450, 462, 455, 480
    ],
    "Type": "Historical"
})

forecast_data = pd.DataFrame({
    "Year": list(range(2026, 2031)),
    "Value": [495, 510, 520, 540, 555],
    "Lower Bound": [475, 485, 490, 505, 515],
    "Upper Bound": [515, 535, 550, 575, 595],
    "Type": "Predicted"
})


st.divider()
st.subheader("Forecast Visualisation")
st.caption(
    "Compare historical observations with predicted future values."
)

fig_forecast = px.line(
    historical_data,
    x="Year",
    y="Value",
    markers=True
)

fig_forecast.update_traces(
    name="Historical Data",
    line_color="#00B8D9",
    line_width=3
)

fig_forecast.add_scatter(
    x=forecast_data["Year"],
    y=forecast_data["Value"],
    mode="lines+markers",
    name="Predicted Values",
    line=dict(color="#7955D9", width=3, dash="dash")
)

fig_forecast.add_scatter(
    x=forecast_data["Year"],
    y=forecast_data["Upper Bound"],
    mode="lines",
    line=dict(width=0),
    showlegend=False,
    hoverinfo="skip"
)

fig_forecast.add_scatter(
    x=forecast_data["Year"],
    y=forecast_data["Lower Bound"],
    mode="lines",
    line=dict(width=0),
    fill="tonexty",
    fillcolor="rgba(121, 85, 217, 0.15)",
    name="Confidence Interval",
    hoverinfo="skip"
)

fig_forecast.update_layout(
    template=plotly_template,
    height=500,
    paper_bgcolor=paper_color,
    plot_bgcolor=plot_color,
    font=dict(color=text_color),
    margin=dict(l=20, r=20, t=30, b=20),
    xaxis=dict(showgrid=False, title="Year"),
    yaxis=dict(showgrid=True, gridcolor=grid_color, title="Value"),
    legend_title_text="Data Type"
)

st.plotly_chart(fig_forecast, use_container_width=True)


st.divider()
st.subheader("Model Performance")
st.caption("Evaluate the performance of the selected prediction model.")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="MAE",
        value="18.6"
    )

with col2:
    st.metric(
        label="RMSE",
        value="24.3"
    )

with col3:
    st.metric(
        label="R² Score",
        value="0.89"
    )

with col4:
    st.metric(
        label="MAPE",
        value="4.2%"
    )

st.divider()
st.subheader("Prediction Comparison")
st.caption("Compare predictive models and their projected outcomes.")

comparison_models = st.multiselect(
    "Select Models to Compare",
    [
        "Linear Regression",
        "Random Forest Regressor",
        "ARIMA",
        "Exponential Smoothing"
    ],
    default=[
        "Linear Regression",
        "Random Forest Regressor"
    ]
)

comparison_data = pd.DataFrame({
    "Year": [2026, 2027, 2028, 2029, 2030] * 4,
    "Predicted Value": [
        495, 510, 520, 540, 555,
        490, 505, 525, 535, 565,
        500, 515, 530, 545, 560,
        485, 500, 518, 530, 548
    ],
    "Model": (
        ["Linear Regression"] * 5
        + ["Random Forest Regressor"] * 5
        + ["ARIMA"] * 5
        + ["Exponential Smoothing"] * 5
    )
})

if comparison_models:

    filtered_comparison = comparison_data[
        comparison_data["Model"].isin(comparison_models)
    ]

    fig_comparison = px.line(
        filtered_comparison,
        x="Year",
        y="Predicted Value",
        color="Model",
        markers=True,
        color_discrete_sequence=[
            "#00B8D9",
            "#7955D9",
            "#B87948",
            "#16A36A"
        ]
    )

    fig_comparison.update_layout(
        template=plotly_template,
        height=450,
        paper_bgcolor=paper_color,
        plot_bgcolor=plot_color,
        font=dict(color=text_color),
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor=grid_color),
        legend_title_text="Prediction Model"
    )

    st.plotly_chart(fig_comparison, use_container_width=True)

else:
    st.info("Select at least one model to compare.")


st.divider()
st.subheader("Prediction Insights")
st.caption("Key observations derived from the predictive analysis.")

col1, col2 = st.columns(2)

with col1:
    st.info(
        "**Expected Trend**\n\n"
        "The selected indicator is projected to show "
        "an overall increasing trend throughout the forecast period."
    )

with col2:
    st.info(
        "**Model Performance**\n\n"
        "The selected prediction model demonstrates "
        "a relatively strong fit to the historical data."
    )


st.divider()
st.subheader("Export Analysis")
st.caption("Download prediction results for further analysis.")

col1, col2 = st.columns(2)

with col1:
    st.download_button(
        label="Forecast Results",
        data=forecast_data.to_csv(index=False).encode("utf-8"),
        file_name="forecast_results.csv",
        mime="text/csv",
        use_container_width=True
    )

with col2:
    st.download_button(
        label="Model Comparison",
        data=comparison_data.to_csv(index=False).encode("utf-8"),
        file_name="model_comparison.csv",
        mime="text/csv",
        use_container_width=True
    )



