
import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Territorial Intelligence Hub",
    page_icon="🌍",
    layout="wide"
)

dark_mode = st.session_state.get("dark_mode", False)

plotly_template = "plotly_dark" if dark_mode else "plotly_white"
text_color = "#E2E8F0" if dark_mode else "#263746"
grid_color = "#344454" if dark_mode else "#E2E8F0"
paper_color = "#1B2732" if dark_mode else "#FFFFFF"
plot_color = "#1B2732" if dark_mode else "#FFFFFF"


def apply_chart_theme(fig):
    fig.update_layout(
        template=plotly_template,
        font=dict(color=text_color),
        paper_bgcolor=paper_color,
        plot_bgcolor=plot_color,
        margin=dict(l=20, r=20, t=35, b=20),
        legend_title_text=""
    )

    fig.update_xaxes(
        gridcolor=grid_color,
        zerolinecolor=grid_color
    )

    fig.update_yaxes(
        gridcolor=grid_color,
        zerolinecolor=grid_color
    )

    return fig


# --------------------------------------------------
# MOCK DATA
# --------------------------------------------------

# Temporary synthetic data.
# Replace with application services when the backend is ready.

territories = {
    "Guarda": (40.5373, -7.2676),
    "Covilhã": (40.2860, -7.5030),
    "Lisboa": (38.7223, -9.1393),
    "Porto": (41.1579, -8.6291),
    "Braga": (41.5454, -8.4265),
    "Aveiro": (40.6405, -8.6538),
    "Coimbra": (40.2033, -8.4103),
    "Viseu": (40.6566, -7.9125),
    "Faro": (37.0194, -7.9304),
    "Leiria": (39.7436, -8.8071),
    "Évora": (38.5714, -7.9135),
    "Beja": (38.0151, -7.8632),
    "Setúbal": (38.5244, -8.8882),
    "Viana do Castelo": (41.6918, -8.8344),
    "Vila Real": (41.3006, -7.7441),
    "Bragança": (41.8061, -6.7567),
    "Santarém": (39.2362, -8.6850),
    "Castelo Branco": (39.8222, -7.4909)
}

base_data = pd.DataFrame({
    "Territory": list(territories.keys()),
    "Energy Consumption": [
        420, 310, 890, 760, 580, 390, 470, 350, 280,
        330, 240, 210, 410, 290, 260, 180, 320, 270
    ],
    "Energy Production": [
        120, 95, 180, 150, 140, 110, 130, 100, 190,
        125, 170, 185, 145, 105, 115, 90, 110, 160
    ],
    "Economic Activity": [
        68, 54, 95, 91, 82, 72, 76, 61, 70,
        65, 58, 52, 74, 57, 55, 46, 63, 50
    ]
})

base_data["Latitude"] = base_data["Territory"].map(
    lambda x: territories[x][0]
)

base_data["Longitude"] = base_data["Territory"].map(
    lambda x: territories[x][1]
)

# Synthetic annual variation values
base_data["Variation (%)"] = [
    8.2, -4.5, 5.8, 2.1, 7.4, -2.8, 3.5, -5.2, 9.1,
    1.8, -3.4, 6.7, 4.2, -1.5, 5.3, -6.1, 2.6, 7.8
]

# Generate a synthetic historical trend
historical_data = []

for _, row in base_data.iterrows():
    for year in range(2020, 2027):
        factor = 1 + ((year - 2020) * 0.018)
        value = row["Energy Consumption"] * factor

        historical_data.append({
            "Territory": row["Territory"],
            "Year": year,
            "Energy Consumption": round(value, 2),
            "Energy Production": round(
                row["Energy Production"] * (1 + (year - 2020) * 0.025), 2
            ),
            "Economic Activity": round(
                row["Economic Activity"] * (1 + (year - 2020) * 0.012), 2
            )
        })

historical_data = pd.DataFrame(historical_data)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("Territorial Intelligence Hub")

st.caption(
    "Monitor territorial indicators, identify relevant changes "
    "and access analytical insights."
)

st.divider()

st.info(
    "Prototype using synthetic data. Indicators, variations and "
    "territorial signals are illustrative and do not represent "
    "real measurements."
)


# --------------------------------------------------
# TERRITORIAL PULSE
# --------------------------------------------------

st.subheader("Territorial Pulse")

total_territories = len(base_data)

signals = base_data[
    (base_data["Variation (%)"] >= 5) |
    (base_data["Variation (%)"] <= -5)
]

average_variation = base_data["Variation (%)"].mean()

positive_variations = len(
    base_data[base_data["Variation (%)"] > 0]
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Territories Monitored",
        total_territories
    )

with col2:
    st.metric(
        "Relevant Signals",
        len(signals)
    )

with col3:
    st.metric(
        "Average Variation",
        f"{average_variation:+.1f}%"
    )

with col4:
    st.metric(
        "Positive Variations",
        f"{positive_variations}/{total_territories}"
    )


st.divider()


# --------------------------------------------------
# TERRITORIAL SIGNALS
# --------------------------------------------------

st.subheader("Territorial Signals")

st.caption(
    "Illustrative signals based on variations in the selected indicator."
)

signal_data = base_data.copy()

signal_data["Signal"] = signal_data["Variation (%)"].apply(
    lambda x: (
        "Significant increase" if x >= 5
        else "Significant decrease" if x <= -5
        else "Moderate variation"
    )
)

signal_data["Priority"] = signal_data["Variation (%)"].apply(
    lambda x: (
        "High" if abs(x) >= 7
        else "Medium" if abs(x) >= 5
        else "Low"
    )
)

high_signals = signal_data[
    signal_data["Priority"] == "High"
]

medium_signals = signal_data[
    signal_data["Priority"] == "Medium"
]

signal_col1, signal_col2 = st.columns(2)

with signal_col1:
    st.markdown("##### Territories requiring attention")

    if not high_signals.empty:
        for _, row in high_signals.iterrows():
            with st.container(border=True):
                st.markdown(
                    f"**{row['Territory']}**"
                )

                st.write(
                    f"{row['Signal']} — "
                    f"{row['Variation (%)']:+.1f}%"
                )

                st.caption(
                    f"Illustrative priority: {row['Priority']}"
                )
    else:
        st.success("No relevant signals detected.")

with signal_col2:
    st.markdown("##### Other relevant variations")

    if not medium_signals.empty:
        for _, row in medium_signals.iterrows():
            with st.container(border=True):
                st.markdown(
                    f"**{row['Territory']}**"
                )

                st.write(
                    f"{row['Signal']} — "
                    f"{row['Variation (%)']:+.1f}%"
                )

                st.caption(
                    f"Illustrative priority: {row['Priority']}"
                )
    else:
        st.info("No additional variations detected.")


st.divider()


# --------------------------------------------------
# GEOGRAPHICAL OVERVIEW
# --------------------------------------------------

st.subheader("Geographical Overview")

map_col1, map_col2 = st.columns([2, 1])

with map_col1:
    selected_map_indicator = st.selectbox(
        "Indicator to display",
        [
            "Energy Consumption",
            "Energy Production",
            "Economic Activity"
        ],
        key="hub_map_indicator"
    )

    map_data = base_data.copy()

    portugal_map = folium.Map(
        location=[39.6, -8.0],
        zoom_start=6,
        tiles="OpenStreetMap"
    )

    min_value = map_data[selected_map_indicator].min()
    max_value = map_data[selected_map_indicator].max()

    for _, row in map_data.iterrows():

        value = row[selected_map_indicator]

        if max_value == min_value:
            radius = 8
        else:
            radius = 5 + (
                (value - min_value) /
                (max_value - min_value)
            ) * 10

        variation = row["Variation (%)"]

        if variation >= 5:
            marker_color = "#DC6B6B"
        elif variation <= -5:
            marker_color = "#4C91D9"
        else:
            marker_color = "#D6A84B"

        folium.CircleMarker(
            location=[
                row["Latitude"],
                row["Longitude"]
            ],
            radius=radius,
            color=marker_color,
            fill=True,
            fill_color=marker_color,
            fill_opacity=0.75,
            tooltip=row["Territory"],
            popup=(
                f"<b>{row['Territory']}</b><br>"
                f"{selected_map_indicator}: {value}<br>"
                f"Variation: {variation:+.1f}%"
            )
        ).add_to(portugal_map)

    st_folium(
        portugal_map,
        width=None,
        height=480,
        key="territorial_hub_map"
    )

    st.caption(
        "Markers represent approximate municipality locations. "
        "Official administrative boundaries are not yet integrated."
    )

with map_col2:
    st.markdown("##### Map interpretation")

    st.markdown(
        """
        **Marker size**

        Represents the relative value of the selected indicator.

        **Marker colour**

        - 🔴 Significant increase
        - 🔵 Significant decrease
        - 🟡 Moderate variation
        """
    )

    st.divider()

    st.markdown("##### Indicator summary")

    st.metric(
        "Average value",
        f"{map_data[selected_map_indicator].mean():.1f}"
    )

    st.metric(
        "Highest value",
        map_data[selected_map_indicator].max()
    )

    st.metric(
        "Lowest value",
        map_data[selected_map_indicator].min()
    )


st.divider()


# --------------------------------------------------
# INDICATOR MONITORING
# --------------------------------------------------

st.subheader("Indicator Monitoring")

st.caption(
    "Follow the historical evolution of a territorial indicator."
)

monitor_col1, monitor_col2 = st.columns([1, 2])

with monitor_col1:
    monitored_indicator = st.selectbox(
        "Indicator",
        [
            "Energy Consumption",
            "Energy Production",
            "Economic Activity"
        ],
        key="hub_monitor_indicator"
    )

    monitoring_scope = st.selectbox(
        "Monitoring scope",
        [
            "National",
            "Individual territory"
        ]
    )

    if monitoring_scope == "Individual territory":
        monitored_territory = st.selectbox(
            "Territory",
            base_data["Territory"].tolist()
        )
    else:
        monitored_territory = None

with monitor_col2:

    trend_data = historical_data.copy()

    if monitored_territory:
        trend_data = trend_data[
            trend_data["Territory"] == monitored_territory
        ]

        fig = px.line(
            trend_data,
            x="Year",
            y=monitored_indicator,
            markers=True,
            title=f"{monitored_indicator} — {monitored_territory}"
        )

    else:
        national_trend = (
            trend_data.groupby("Year")[monitored_indicator]
            .mean()
            .reset_index()
        )

        fig = px.line(
            national_trend,
            x="Year",
            y=monitored_indicator,
            markers=True,
            title=f"National average — {monitored_indicator}"
        )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title=monitored_indicator
    )

    apply_chart_theme(fig)

    st.plotly_chart(
        fig,
        use_container_width=True
    )


st.divider()


# --------------------------------------------------
# MONITORING SUMMARY
# --------------------------------------------------

st.subheader("Territorial Monitoring Summary")

summary_data = signal_data[
    [
        "Territory",
        "Energy Consumption",
        "Energy Production",
        "Economic Activity",
        "Variation (%)",
        "Signal",
        "Priority"
    ]
].copy()

summary_data = summary_data.sort_values(
    by="Variation (%)",
    key=lambda x: x.abs(),
    ascending=False
)

st.dataframe(
    summary_data,
    use_container_width=True,
    hide_index=True
)

csv = summary_data.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Export Monitoring Data",
    data=csv,
    file_name="territorial_monitoring.csv",
    mime="text/csv"
)


st.divider()


# --------------------------------------------------
# ANALYTICAL SHORTCUTS
# --------------------------------------------------

st.subheader("Explore Further")

st.caption(
    "Access the analytical modules for a deeper investigation "
    "of territorial patterns."
)

shortcut_col1, shortcut_col2 = st.columns(2)

with shortcut_col1:
    with st.container(border=True):
        st.markdown("##### Statistical Analysis")
        st.write(
            "Explore distributions, descriptive statistics "
            "and relationships between indicators."
        )
        st.page_link(
            "pages/statistical_analysis.py",
            label="Open Statistical Analysis",
            icon="📊"
        )

    with st.container(border=True):
        st.markdown("##### Clustering")
        st.write(
            "Identify groups of territories with similar "
            "characteristics."
        )
        st.page_link(
            "pages/clustering.py",
            label="Open Clustering",
            icon="🔗"
        )

with shortcut_col2:
    with st.container(border=True):
        st.markdown("##### Predictions")
        st.write(
            "Explore forecasts and potential future "
            "developments in territorial indicators."
        )
        st.page_link(
            "pages/predictions.py",
            label="Open Predictions",
            icon="📈"
        )

    with st.container(border=True):
        st.markdown("##### Comparisons")
        st.write(
            "Compare indicators, territories and their "
            "evolution over time."
        )
        st.page_link(
            "pages/comparisons.py",
            label="Open Comparisons",
            icon="⚖️"
        )


# --------------------------------------------------
# DATA STATUS
# --------------------------------------------------

with st.expander("Data Sources & Limitations"):

    st.markdown(
        """
        **Current prototype**

        - All values are synthetic.
        - Territorial coordinates are approximate.
        - Variations and signal priorities are illustrative.
        - Historical values are generated for demonstration.
        - No real datasets are currently connected.

        **Planned integration**

        - E-REDES energy consumption datasets.
        - E-REDES decentralised energy production datasets.
        - PORDATA socioeconomic indicators.
        - Official administrative boundaries (CAOP).

        **Future architecture**

        The page will consume processed data and monitoring
        results through the application services layer.
        Data acquisition, transformations and analytical
        calculations will remain outside the Streamlit page.
        """
    )
