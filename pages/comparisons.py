
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# =========================================================
# THEME CONFIGURATION
# =========================================================

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


def apply_chart_theme(fig):
    """Apply the application's theme to a Plotly figure."""

    fig.update_layout(
        template=plotly_template,
        paper_bgcolor=paper_color,
        plot_bgcolor=plot_color,
        font_color=text_color,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    fig.update_xaxes(gridcolor=grid_color)
    fig.update_yaxes(gridcolor=grid_color)

    return fig


# =========================================================
# PAGE HEADER
# =========================================================

st.title("Comparisons")

st.caption(
    "Compare territorial indicators and explore "
    "differences across regions and time periods."
)

st.divider()


# =========================================================
# COMPARISON CONFIGURATION
# =========================================================

st.subheader("Comparison Configuration")
st.caption("Define the parameters for your comparison.")

comparison_type = st.selectbox(
    "Comparison Type",
    [
        "Territory Comparison",
        "Indicator Comparison",
        "Time Period Comparison"
    ]
)

indicators = [
    "Energy Consumption",
    "Population Density",
    "Economic Activity",
    "Renewable Energy Production"
]

territories = [
    "Guarda",
    "Covilhã",
    "Lisboa",
    "Porto",
    "Braga",
    "Aveiro",
    "Coimbra",
    "Viseu"
]

# Territory and indicator selection
if comparison_type == "Territory Comparison":

    indicator = st.selectbox(
        "Indicator",
        indicators
    )

    selected_territories = st.multiselect(
        "Select Territories to Compare",
        territories,
        default=["Guarda", "Covilhã"]
    )

elif comparison_type == "Indicator Comparison":

    territory = st.selectbox(
        "Territory",
        ["All Territories"] + territories
    )

    selected_indicators = st.multiselect(
        "Select Indicators to Compare",
        indicators,
        default=[
            "Energy Consumption",
            "Economic Activity"
        ]
    )

else:

    indicator = st.selectbox(
        "Indicator",
        indicators
    )

    territory = st.selectbox(
        "Territory",
        ["All Territories"] + territories
    )

    col1, col2 = st.columns(2)

    with col1:
        start_year = st.selectbox(
            "First Period",
            range(2000, 2027),
            index=0
        )

    with col2:
        end_year = st.selectbox(
            "Second Period",
            range(2000, 2027),
            index=6
        )

    if start_year >= end_year:
        st.error("The second period must be later than the first.")


# =========================================================
# TEMPORARY MOCK DATA
# =========================================================

# Demonstration data only — to be replaced by real datasets.

np.random.seed(42)

years = list(range(2000, 2027))

mock_data = pd.DataFrame({
    "Territory": territories * len(years),
    "Year": [
        year
        for year in years
        for _ in territories
    ]
})

mock_data["Energy Consumption"] = np.random.randint(
    200, 900, len(mock_data)
)

mock_data["Population Density"] = np.random.randint(
    50, 1000, len(mock_data)
)

mock_data["Economic Activity"] = np.random.randint(
    100, 800, len(mock_data)
)

mock_data["Renewable Energy Production"] = np.random.randint(
    50, 600, len(mock_data)
)


# =========================================================
# COMPARISON OVERVIEW
# =========================================================

st.divider()

st.subheader("Comparison Overview")
st.caption("Summary of the selected comparison.")

if comparison_type == "Territory Comparison":

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Territories Selected",
            len(selected_territories)
        )

    with col2:
        st.metric(
            "Indicator",
            indicator
        )

    with col3:
        st.metric(
            "Reference Year",
            "2025"
        )

elif comparison_type == "Indicator Comparison":

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Indicators Selected",
            len(selected_indicators)
        )

    with col2:
        st.metric(
            "Territory",
            territory
        )

    with col3:
        st.metric(
            "Reference Year",
            "2025"
        )

else:

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Indicator",
            indicator
        )

    with col2:
        st.metric(
            "First Period",
            start_year
        )

    with col3:
        st.metric(
            "Second Period",
            end_year
        )


# =========================================================
# VISUAL COMPARISON
# =========================================================

st.divider()

st.subheader("Visual Comparison")
st.caption("Visualise differences across the selected comparison.")


# Territory Comparison
if comparison_type == "Territory Comparison":

    if selected_territories:

        comparison_data = mock_data[
            (mock_data["Territory"].isin(selected_territories)) &
            (mock_data["Year"] == 2025)
        ]

        fig_comparison = px.bar(
            comparison_data,
            x="Territory",
            y=indicator,
            color="Territory",
            text_auto=".2s",
            color_discrete_sequence=[
                "#00B8D9",
                "#7955D9",
                "#B87948",
                "#16A36A",
                "#E5A000"
            ]
        )

        fig_comparison.update_layout(
            xaxis_title="Territory",
            yaxis_title=indicator,
            showlegend=False
        )

        apply_chart_theme(fig_comparison)

        st.plotly_chart(
            fig_comparison,
            use_container_width=True
        )

    else:
        st.info("Select at least one territory to compare.")


# Indicator Comparison
elif comparison_type == "Indicator Comparison":

    if selected_indicators:

        comparison_data = mock_data[
            mock_data["Year"] == 2025
        ]

        if territory != "All Territories":

            comparison_data = comparison_data[
                comparison_data["Territory"] == territory
            ]

            indicator_values = comparison_data[
                selected_indicators
            ].iloc[0]

        else:

            indicator_values = comparison_data[
                selected_indicators
            ].mean()

        indicator_data = indicator_values.reset_index()

        indicator_data.columns = [
            "Indicator",
            "Value"
        ]

        fig_comparison = px.bar(
            indicator_data,
            x="Indicator",
            y="Value",
            color="Indicator",
            text_auto=".2s",
            color_discrete_sequence=[
                "#00B8D9",
                "#7955D9",
                "#B87948",
                "#16A36A"
            ]
        )

        fig_comparison.update_layout(
            xaxis_title="Indicator",
            yaxis_title="Value",
            showlegend=False
        )

        apply_chart_theme(fig_comparison)

        st.plotly_chart(
            fig_comparison,
            use_container_width=True
        )

    else:
        st.info("Select at least one indicator to compare.")


# Time Period Comparison
else:

    if start_year < end_year:

        period_data = mock_data[
            mock_data["Year"].isin([start_year, end_year])
        ]

        if territory != "All Territories":

            period_data = period_data[
                period_data["Territory"] == territory
            ]

        else:

            period_data = (
                period_data
                .groupby("Year", as_index=False)[indicator]
                .mean()
            )

        fig_comparison = px.bar(
            period_data,
            x="Year",
            y=indicator,
            color="Year",
            text_auto=".2s",
            barmode="group",
            color_discrete_sequence=[
                "#00B8D9",
                "#7955D9"
            ]
        )

        fig_comparison.update_layout(
            xaxis_title="Year",
            yaxis_title=indicator,
            showlegend=False
        )

        apply_chart_theme(fig_comparison)

        st.plotly_chart(
            fig_comparison,
            use_container_width=True
        )


# =========================================================
# GEOGRAPHICAL COMPARISON
# =========================================================

st.divider()

st.subheader("Geographical Comparison")

st.caption(
    "Explore the spatial distribution of the selected indicators."
)

col1, col2 = st.columns(2)

with col1:

    st.markdown("**Comparison A**")

    st.info(
        "Geographical visualisation will be displayed here "
        "once territorial boundary data is integrated."
    )

with col2:

    st.markdown("**Comparison B**")

    st.info(
        "The second geographical view will allow spatial "
        "differences between territories or indicators to be explored."
    )


# =========================================================
# COMPARISON INSIGHTS
# =========================================================

st.divider()

st.subheader("Comparison Insights")

st.caption("Key observations from the selected comparison.")

if comparison_type == "Territory Comparison":

    if selected_territories:

        st.info(
            f"The comparison explores **{indicator}** across "
            f"{len(selected_territories)} selected territories. "
            "Use the visualisation above to identify differences "
            "between regions."
        )

    else:
        st.info("Select territories to generate comparison insights.")


elif comparison_type == "Indicator Comparison":

    if selected_indicators:

        st.info(
            f"The comparison explores {len(selected_indicators)} "
            f"indicators within **{territory}**. "
            "Observe the relative differences between the selected indicators."
        )

    else:
        st.info("Select indicators to generate comparison insights.")


else:

    if start_year < end_year:

        st.info(
            f"This comparison analyses changes in **{indicator}** "
            f"between {start_year} and {end_year} "
            f"for **{territory}**."
        )

    else:
        st.info("Select a valid time period to generate comparison insights.")


# =========================================================
# EXPORT COMPARISON
# =========================================================

st.divider()

st.subheader("Export Comparison")

st.caption("Download the data used in the current comparison.")


if comparison_type == "Territory Comparison":

    export_data = mock_data[
        (mock_data["Territory"].isin(selected_territories)) &
        (mock_data["Year"] == 2025)
    ].copy()


elif comparison_type == "Indicator Comparison":

    comparison_data = mock_data[
        mock_data["Year"] == 2025
    ]

    if territory != "All Territories":

        export_data = comparison_data[
            comparison_data["Territory"] == territory
        ][["Territory", "Year"] + selected_indicators].copy()

    else:

        export_data = (
            comparison_data
            .groupby("Year", as_index=False)[selected_indicators]
            .mean()
        )

        export_data.insert(
            0,
            "Territory",
            "All Territories"
        )

else:

    export_data = mock_data[
        mock_data["Year"].isin([start_year, end_year])
    ].copy()

    if territory != "All Territories":

        export_data = export_data[
            export_data["Territory"] == territory
        ].copy()

    else:

        export_data = (
            export_data
            .groupby("Year", as_index=False)[[indicator]]
            .mean()
        )

        export_data.insert(
            0,
            "Territory",
            "All Territories"
        )


st.download_button(
    label="Download Comparison Data",
    data=export_data.to_csv(index=False),
    file_name="locus_ai_comparison.csv",
    mime="text/csv"
)
