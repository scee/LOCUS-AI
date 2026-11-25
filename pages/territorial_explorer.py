
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium

from streamlit_folium import st_folium


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

    fig.update_layout(
        template=plotly_template,
        paper_bgcolor=paper_color,
        plot_bgcolor=plot_color,
        font_color=text_color,
        margin=dict(l=20, r=20, t=35, b=20)
    )

    fig.update_xaxes(gridcolor=grid_color)
    fig.update_yaxes(gridcolor=grid_color)

    return fig


# =========================================================
# PAGE HEADER
# =========================================================

st.title("Territorial Explorer")

st.caption(
    "Territorial Intelligence Workspace | "
    "Explore, investigate and understand territorial patterns."
)

st.divider()


# =========================================================
# TEMPORARY TERRITORIAL DATA
# =========================================================

# Demonstration data only.
# Replace with application service results when integrated.

territories = [
    "Guarda",
    "Covilhã",
    "Lisboa",
    "Porto",
    "Braga",
    "Aveiro",
    "Coimbra",
    "Viseu",
    "Faro",
    "Leiria",
    "Évora",
    "Beja",
    "Setúbal",
    "Viana do Castelo",
    "Vila Real",
    "Bragança",
    "Santarém",
    "Castelo Branco"
]

indicators = [
    "Energy Consumption",
    "Population Density",
    "Economic Activity",
    "Renewable Energy Production"
]

np.random.seed(42)

territorial_data = pd.DataFrame({
    "Territory": territories,
    "Energy Consumption": np.random.randint(
        200, 900, len(territories)
    ),
    "Population Density": np.random.randint(
        50, 1000, len(territories)
    ),
    "Economic Activity": np.random.randint(
        100, 800, len(territories)
    ),
    "Renewable Energy Production": np.random.randint(
        50, 600, len(territories)
    )
})


# Approximate municipal coordinates for demonstration.
territory_coordinates = {
    "Guarda": [40.5373, -7.2658],
    "Covilhã": [40.2860, -7.5030],
    "Lisboa": [38.7223, -9.1393],
    "Porto": [41.1579, -8.6291],
    "Braga": [41.5454, -8.4265],
    "Aveiro": [40.6405, -8.6538],
    "Coimbra": [40.2033, -8.4103],
    "Viseu": [40.6566, -7.9125],
    "Faro": [37.0194, -7.9304],
    "Leiria": [39.7436, -8.8071],
    "Évora": [38.5714, -7.9135],
    "Beja": [38.0151, -7.8632],
    "Setúbal": [38.5244, -8.8882],
    "Viana do Castelo": [41.6932, -8.8329],
    "Vila Real": [41.3006, -7.7441],
    "Bragança": [41.8061, -6.7567],
    "Santarém": [39.2362, -8.6850],
    "Castelo Branco": [39.8222, -7.4909]
}


# =========================================================
# TERRITORIAL CONTEXT
# =========================================================

st.subheader("Territorial Context")

st.caption(
    "Define the geographical and analytical context of your investigation."
)

with st.container(border=True):

    col1, col2, col3 = st.columns(3)

    with col1:

        selected_territory = st.selectbox(
            "Territory",
            ["All Territories"] + territories
        )

    with col2:

        territorial_level = st.selectbox(
            "Territorial Level",
            [
                "Municipality",
                "District",
                "NUTS II",
                "NUTS III"
            ]
        )

    with col3:

        selected_year = st.selectbox(
            "Reference Year",
            range(2000, 2027),
            index=25
        )

    selected_indicators = st.multiselect(
        "Indicators to Explore",
        indicators,
        default=[
            "Energy Consumption",
            "Economic Activity"
        ]
    )

    main_indicator = st.selectbox(
        "Primary Indicator",
        indicators,
        index=0
    )


# =========================================================
# DATA AVAILABILITY NOTICE
# =========================================================

st.info(
    "Demonstration environment: the current values are synthetic. "
    "Real E-REDES and Pordata datasets, historical coverage and "
    "analytical results will be connected in a later integration phase."
)


# =========================================================
# TERRITORIAL DATA CONTEXT
# =========================================================

if selected_territory == "All Territories":

    context_data = territorial_data.copy()

else:

    context_data = territorial_data[
        territorial_data["Territory"] == selected_territory
    ].copy()


# =========================================================
# WORKSPACE OVERVIEW
# =========================================================

st.divider()

st.subheader("Workspace Overview")

st.caption(
    "A summary of the current territorial investigation."
)

if not context_data.empty:

    territory_count = len(context_data)

    total_consumption = context_data[
        "Energy Consumption"
    ].sum()

    average_density = context_data[
        "Population Density"
    ].mean()

    total_renewable = context_data[
        "Renewable Energy Production"
    ].sum()

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Territories in Scope",
            territory_count
        )

    with col2:

        st.metric(
            "Energy Consumption",
            f"{total_consumption:,.0f} MWh"
        )

    with col3:

        st.metric(
            "Average Population Density",
            f"{average_density:,.0f}"
        )

    with col4:

        st.metric(
            "Renewable Production",
            f"{total_renewable:,.0f} MWh"
        )


# =========================================================
# GEOGRAPHIC EXPLORATION
# =========================================================

st.divider()

st.subheader("Geographic Exploration")

st.caption(
    "Explore the spatial context of the selected territory "
    "and its surrounding municipalities."
)

map_col, context_col = st.columns([1.8, 1])

with map_col:

    st.markdown("**Territorial Map**")

    if selected_territory == "All Territories":

        map_center = [39.7, -8.0]
        zoom_level = 6

    else:

        map_center = territory_coordinates[selected_territory]
        zoom_level = 10

    territorial_map = folium.Map(
        location=map_center,
        zoom_start=zoom_level,
        tiles="OpenStreetMap"
    )

    for territory, coordinates in territory_coordinates.items():

        if (
            selected_territory == "All Territories"
            or territory == selected_territory
        ):

            territory_value = territorial_data.loc[
                territorial_data["Territory"] == territory,
                main_indicator
            ].iloc[0]

            folium.CircleMarker(
                location=coordinates,
                radius=8,
                color="#00B8D9",
                fill=True,
                fill_color="#00B8D9",
                fill_opacity=0.8,
                tooltip=(
                    f"{territory} | "
                    f"{main_indicator}: {territory_value:,.2f}"
                )
            ).add_to(territorial_map)

    st_folium(
        territorial_map,
        use_container_width=True,
        height=480,
        returned_objects=[]
    )

with context_col:

    st.markdown("**Territorial Context**")

    if selected_territory == "All Territories":

        st.markdown("**Portugal — Selected Territories**")

        st.write(
            "The current workspace includes all municipalities "
            "available in the demonstration dataset."
        )

        st.metric(
            "Territories Available",
            len(territories)
        )

    else:

        st.markdown(f"**{selected_territory}**")

        st.write(
            "Explore the selected municipality and its "
            "territorial indicators."
        )

        selected_row = context_data.iloc[0]

        st.metric(
            "Energy Consumption",
            f"{selected_row['Energy Consumption']:,.0f} MWh"
        )

        st.metric(
            "Economic Activity",
            f"{selected_row['Economic Activity']:,.0f}"
        )

    st.divider()

    st.markdown("**Geographic Data Status**")

    st.caption("Current map: approximate point locations")

    st.caption("Administrative boundaries: pending CAOP2025 integration")


# =========================================================
# INDICATOR EXPLORATION
# =========================================================

st.divider()

st.subheader("Indicator Exploration")

st.caption(
    "Investigate how selected indicators are distributed "
    "across the territories in scope."
)

if selected_indicators:

    indicator_view = context_data[
        ["Territory"] + selected_indicators
    ].copy()

    indicator_long = indicator_view.melt(
        id_vars="Territory",
        var_name="Indicator",
        value_name="Value"
    )

    fig_indicators = px.bar(
        indicator_long,
        x="Territory",
        y="Value",
        color="Indicator",
        barmode="group",
        color_discrete_sequence=[
            "#00B8D9",
            "#7955D9",
            "#B87948",
            "#16A36A"
        ]
    )

    fig_indicators.update_layout(
        xaxis_title="Territory",
        yaxis_title="Indicator Value"
    )

    apply_chart_theme(fig_indicators)

    st.plotly_chart(
        fig_indicators,
        use_container_width=True
    )

else:

    st.info(
        "Select at least one indicator to explore its distribution."
    )


# =========================================================
# ANALYTICAL RESULTS
# =========================================================

st.divider()

st.subheader("Analytical Results")

st.caption(
    "Consult outputs produced by the platform's analytical modules."
)

analysis_col, clustering_col = st.columns(2)

with analysis_col:

    with st.container(border=True):

        st.markdown("**Statistical Analysis**")

        st.write(
            "Explore statistical findings associated with "
            "the selected territorial context."
        )

        st.caption("Integration status: pending")

        st.info(
            "Correlation results, descriptive statistics and "
            "other analytical outputs will be displayed here "
            "when the analysis service is integrated."
        )

with clustering_col:

    with st.container(border=True):

        st.markdown("**Clustering Results**")

        st.write(
            "Consult territorial groups identified by "
            "the platform's clustering module."
        )

        st.caption("Integration status: pending")

        st.info(
            "Cluster assignments and territorial profiles "
            "will be displayed here when clustering results "
            "are available."
        )


# =========================================================
# TERRITORIAL INVESTIGATION
# =========================================================

st.divider()

st.subheader("Territorial Investigation")

st.caption(
    "Identify territories that may deserve further investigation."
)

ranking_data = context_data[
    ["Territory", main_indicator]
].sort_values(
    by=main_indicator,
    ascending=False
).reset_index(drop=True)

if not ranking_data.empty:

    ranking_data.index = ranking_data.index + 1
    ranking_data.index.name = "Rank"

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("**Highest Indicator Values**")

        st.dataframe(
            ranking_data.head(5),
            use_container_width=True
        )

    with col2:

        st.markdown("**Lowest Indicator Values**")

        st.dataframe(
            ranking_data.tail(5).sort_values(
                by=main_indicator,
                ascending=True
            ),
            use_container_width=True
        )

    st.caption(
        "Rankings are descriptive only. Higher values do not "
        "necessarily indicate better or worse territorial performance."
    )


# =========================================================
# EVIDENCE AND EXPORT
# =========================================================

st.divider()

st.subheader("Evidence & Export")

st.caption(
    "Prepare the selected territorial data for further analysis."
)

export_data = context_data.copy()

export_data.insert(
    1,
    "Territorial Level",
    territorial_level
)

export_data.insert(
    2,
    "Reference Year",
    selected_year
)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Territories Included",
        len(export_data)
    )

with col2:

    st.metric(
        "Indicators Available",
        len(indicators)
    )

st.download_button(
    label="Export Territorial Evidence",
    data=export_data.to_csv(index=False),
    file_name="locus_ai_territorial_evidence.csv",
    mime="text/csv"
)


# =========================================================
# DATA PROVENANCE
# =========================================================

with st.expander("Data Provenance & Limitations"):

    st.markdown(
        """
        **Current data status**

        - Energy indicators: synthetic demonstration values.
        - Economic indicators: synthetic demonstration values.
        - Demographic indicators: synthetic demonstration values.
        - Geographic coordinates: approximate municipality locations.
        - Administrative boundaries: CAOP2025 integration pending.
        - Statistical analysis: service integration pending.
        - Clustering results: service integration pending.

        **Important**

        The current workspace is a functional UI prototype.
        No real territorial conclusions should be drawn from
        the demonstration data.
        """
    )
