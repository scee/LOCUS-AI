import streamlit as st
import pandas as pd
import plotly.express as px

#######

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


######## Dados ficticios para demonstração

import numpy as np

# Temporary demo data
np.random.seed(42)

distribution_data = pd.DataFrame({
    "Consumption": np.random.normal(
        loc=485,
        scale=86,
        size=150
    )
})



# Page Header
with st.container():
    st.title("Statistical Analysis")
    st.caption(
        "Explore statistical patterns, distributions "
        "and relationships across territorial indicators."
    )

st.divider()

# Analysis Configuration

st.subheader("Analysis Configuration")
st.caption("Select the data you want to investigate.")

col1, col2 = st.columns(2)

with col1:
    indicator = st.selectbox(
        "Indicator",
        [
            "Energy Consumption",
            "Population Density",
            "Economic Activity",
            "Renewable Energy Production"
        ]
    )

with col2:
    territory = st.selectbox(
        "Territory",
        [
            "All Territories",
            "Guarda",
            "Covilhã",
            "Lisboa",
            "Porto",
            "Braga",
            "Aveiro",
            "Coimbra"
        ]
    )

st.markdown("#### Time Period")

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

st.subheader("Descriptive Statistics")
st.caption("Summary statistics for the selected indicator and territory.")


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Mean",
        value="485.6",
    )

with col2:
    st.metric(
        label="Median",
        value="472.0",
    )

with col3:
    st.metric(
        label="Standard Deviation",
        value="86.4",
    )

with col4:
    st.metric(
        label="Variance",
        value="7464.96",
    )

st.divider()

st.subheader("Statistical Distribution")
st.caption("Explore the distribution and spread of the selected indicator.")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Value Distribution")

    fig_hist = px.histogram(
        distribution_data,
        x="Consumption",
        nbins=20,
        labels={
            "Consumption": "Energy Consumption (MWh)"
        }
    )

    fig_hist.update_traces(
        marker_color="#00B8D9",
        marker_line_color="#FFFFFF",
        marker_line_width=1
    )

    fig_hist.update_layout(
        template=plotly_template,
        height=350,
        paper_bgcolor=paper_color,
        plot_bgcolor=plot_color,
        font=dict(color=text_color),
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False
    )

    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    st.markdown("#### Consumption Trend")

    trend_data = pd.DataFrame({
        "Year": list(range(2010, 2027)),
        "Consumption": [
            390, 405, 398, 420, 435,
            428, 450, 462, 455, 470,
            480, 475, 490, 505, 498,
            515, 530
        ]
    })

    fig_trend = px.line(
        trend_data,
        x="Year",
        y="Consumption",
        markers=True,
        labels={
            "Year": "Year",
            "Consumption": "Energy Consumption (MWh)"
        }
    )

    fig_trend.update_traces(
        line_color="#7955D9",
        marker_color="#7955D9",
        line_width=3
    )

    fig_trend.update_layout(
        template=plotly_template,
        height=350,
        paper_bgcolor=paper_color,
        plot_bgcolor=plot_color,
        font=dict(color=text_color),
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False,
        xaxis=dict(showgrid=False, title=None),
        yaxis=dict(
            showgrid=True,
            gridcolor=grid_color,
            title=None
        )
    )

    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown("#### Statistical Spread")

    fig_box = px.box(
        distribution_data,
        y="Consumption",
        points="outliers",
        labels={
            "Consumption": "Energy Consumption (MWh)"
        }
    )

    fig_box.update_traces(
        marker_color="#7955D9",
        line_color="#7955D9"
    )

    fig_box.update_layout(
        template=plotly_template,
        height=350,
        paper_bgcolor=paper_color,
        plot_bgcolor=plot_color,
        font=dict(color=text_color),
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False
    )

st.plotly_chart(fig_box, use_container_width=True)

st.divider()
st.subheader("Correlation Analysis")
st.caption("Explore relationships between two territorial indicators.")

col1, col2 = st.columns(2)

with col1:
    x_indicator = st.selectbox(
        "First Indicator",
        ["Energy Consumption", "Population Density", "Economic Activity"]
    )

with col2:
    y_indicator = st.selectbox(
        "Second Indicator",
        ["Economic Activity", "Population Density", "Renewable Energy Production"]
    )

# Correlation Data — Temporary Mock Data
np.random.seed(42)

correlation_data = pd.DataFrame({
    "Territory": [
        "Guarda", "Covilhã", "Lisboa", "Porto",
        "Braga", "Aveiro", "Coimbra", "Viseu"
    ],
    "Energy Consumption": np.random.randint(200, 900, 8),
    "Economic Activity": np.random.randint(100, 800, 8),
    "Population Density": np.random.randint(50, 1000, 8),
    "Renewable Energy Production": np.random.randint(50, 600, 8)
})

fig_correlation = px.scatter(
    correlation_data,
    x=x_indicator,
    y=y_indicator,
    text="Territory",
    labels={
        x_indicator: x_indicator,
        y_indicator: y_indicator
    }
)

fig_correlation.update_traces(
    marker=dict(size=12, color="#00B8D9"),
    textposition="top center"
)

fig_correlation.update_layout(
    template=plotly_template,
    height=450,
    paper_bgcolor=paper_color,
    plot_bgcolor=plot_color,
    font=dict(color=text_color),
    margin=dict(l=20, r=20, t=20, b=20),
    showlegend=False,
    xaxis=dict(showgrid=True, gridcolor=grid_color),
    yaxis=dict(showgrid=True, gridcolor=grid_color)
)

st.plotly_chart(fig_correlation, use_container_width=True)

st.markdown("#### Correlation Strength")

if x_indicator != y_indicator:

    correlation = correlation_data[x_indicator].corr(
        correlation_data[y_indicator]
    )

    if correlation >= 0.7:
        strength = "Strong Positive"
    elif correlation >= 0.3:
        strength = "Moderate Positive"
    elif correlation > -0.3:
        strength = "Weak"
    elif correlation > -0.7:
        strength = "Moderate Negative"
    else:
        strength = "Strong Negative"

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Pearson Correlation",
            value=f"{correlation:.2f}"
        )

    with col2:
        st.metric(
            label="Relationship Strength",
            value=strength
        )

else:
    st.warning("Select two different indicators to calculate correlation.")


st.divider()
st.subheader("Correlation Matrix")
st.caption("Explore correlations between all available indicators.")

indicators = [
    "Energy Consumption",
    "Economic Activity",
    "Population Density",
    "Renewable Energy Production"
]

correlation_matrix = correlation_data[indicators].corr()

fig_matrix = px.imshow(
    correlation_matrix,
    text_auto=".2f",
    color_continuous_scale="RdBu",
    color_continuous_midpoint=0,
    zmin=-1,
    zmax=1,
    aspect="auto"
)

fig_matrix.update_layout(
    template=plotly_template,
    height=450,
    paper_bgcolor=paper_color,
    plot_bgcolor=plot_color,
    font=dict(color=text_color),
    coloraxis_colorbar=dict(title="Correlation"),
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(fig_matrix, use_container_width=True)

st.divider()
st.subheader("Data Coverage")
st.caption("Overview of the data available for the selected analysis.")

total_territories = correlation_data["Territory"].nunique()
total_observations = len(correlation_data)
data_completeness = (
    correlation_data[indicators].notna().sum().sum()
    / correlation_data[indicators].size
) * 100

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Territories", total_territories)

with col2:
    st.metric("Observations", total_observations)

with col3:
    st.metric("Time Period", f"{start_year}–{end_year}")

with col4:
    st.metric("Data Completeness", f"{data_completeness:.1f}%")


st.divider()
st.subheader("Export Analysis")
st.caption("Download the data and statistical results.")

# Descriptive Statistics
descriptive_export = correlation_data[indicators].describe().T

# Correlation Matrix
correlation_export = correlation_matrix

# Territory Data
territory_export = correlation_data

col1, col2, col3 = st.columns(3)

with col1:
    st.download_button(
        label="Descriptive Statistics",
        data=descriptive_export.to_csv().encode("utf-8"),
        file_name="descriptive_statistics.csv",
        mime="text/csv",
        use_container_width=True
    )

with col2:
    st.download_button(
        label="Correlation Matrix",
        data=correlation_export.to_csv().encode("utf-8"),
        file_name="correlation_matrix.csv",
        mime="text/csv",
        use_container_width=True
    )

with col3:
    st.download_button(
        label="Territorial Data",
        data=territory_export.to_csv(index=False).encode("utf-8"),
        file_name="territorial_data.csv",
        mime="text/csv",
        use_container_width=True
    )

st.divider()
st.subheader("Statistical Insights")
st.caption("Key observations derived from the statistical analysis.")

col1, col2 = st.columns(2)

with col1:
    st.info(
        "**Energy Consumption**\n\n"
        "The selected indicator shows an overall increasing trend "
        "throughout the analysed period."
    )

with col2:
    st.info(
        "**Territorial Relationship**\n\n"
        "The selected indicators show a potential positive relationship "
        "across the analysed territories."
    )