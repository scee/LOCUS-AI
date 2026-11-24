############ IMPORTS ############

import streamlit as st

import plotly.express as px
import pandas as pd             


dark_mode = st.session_state.get("dark_mode", False)

if dark_mode:
    plotly_template = "plotly_dark"
    grid_color = "#344454"
    text_color = "#E2E8F0"
    paper_color = "#1B2732"
    plot_color = "#1B2732"
    fill_color = "rgba(0, 184, 217, 0.20)"

else:
    plotly_template = "plotly_white"
    grid_color = "#E2E8F0"
    text_color = "#263746"
    paper_color = "#FFFFFF"
    plot_color = "#FFFFFF"
    fill_color = "rgba(0, 184, 217, 0.12)"

##################
# Temporary demo data
energy_data = pd.DataFrame({
    "Month": [
        "Jan", "Feb", "Mar", "Apr",
        "May", "Jun", "Jul", "Aug",
        "Sep", "Oct", "Nov", "Dec"
    ],
    "Consumption": [
        420, 390, 410, 450,
        480, 520, 560, 545,
        490, 460, 430, 470
    ]
})


########################
# Dashboard Header
with st.container():
    st.title("Dashboard")
    st.caption(
        "Territorial Intelligence | "
        "Energy consumption and territorial indicators"
    )

st.divider()


# Key Metrics
st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Energy Consumption",
        value="—",
        delta=None
    )

with col2:
    st.metric(
        label="Territories Analysed",
        value="—",
        delta=None
    )

with col3:
    st.metric(
        label="Available Indicators",                                           
        value="—",
        delta=None
    )


    ##

st.divider()   

st.subheader("Energy Overview")
st.caption("Monthly electricity consumption overview.")

fig = px.area(
    energy_data,
    x="Month",
    y="Consumption",
    markers=True,
    labels={
        "Month": "Month",
        "Consumption": "Energy Consumption (MWh)"
    }
)

fig.update_traces(
    line_color="#00B8D9",
    fillcolor=fill_color,
    ##marker=dict(size=8, color="#00B8D9")
)

fig.update_layout(
    template=plotly_template,
    height=350,
    margin=dict(l=20, r=20, t=20, b=20),
    showlegend=False,
    paper_bgcolor=paper_color,
    plot_bgcolor=plot_color,
    font=dict(color=text_color),

    xaxis=dict(
    showgrid=False,
    title=None
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor=grid_color,
        title=None,
        zeroline=False
    ),

)

st.plotly_chart(
    fig,
    use_container_width=True
)
######################################


st.divider()

st.subheader("Territorial Overview")
st.caption("Explore and compare energy consumption across territories.")

col1, col2 = st.columns([1.5, 1])

with col1:
    st.markdown("#### Energy Consumption by Territory")

    territorial_data = pd.DataFrame({
        "Territory": [
            "Lisboa",
            "Porto",
            "Braga",
            "Aveiro",
            "Coimbra"
        ],
        "Consumption": [850, 720, 590, 480, 410]
    })

    fig_territory = px.bar(
        territorial_data,
        x="Consumption",
        y="Territory",
        orientation="h",
        labels={
            "Consumption": "Consumption (MWh)",
            "Territory": ""
        }
    )

    fig_territory.update_traces(
        marker_color="#00B8D9"
    )

    fig_territory.update_layout(
        template=plotly_template,
        height=350,
        margin=dict(l=10, r=20, t=20, b=20),
        showlegend=False,
        paper_bgcolor=paper_color,
        plot_bgcolor=plot_color,
        font=dict(color=text_color),
        yaxis=dict(autorange="reversed"),
        xaxis=dict(showgrid=True, gridcolor=grid_color)
    )

    st.plotly_chart(
        fig_territory,
        use_container_width=True
    )

    with col2:
        st.markdown("#### Geographic Distribution")

    st.container(border=True).markdown(
        """
        <div style="
            height: 290px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: #718096;
            text-align: center;
        ">
            <div style="font-size: 3rem;">🗺️</div>
            <div style="font-weight: 600; color: #101820;">
                Territorial Map
            </div>
            <div style="font-size: 0.85rem;">
                Geographic data pending
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()

st.subheader("Data & Platform Status")
st.caption("Overview of data sources and analytical components.")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Data Sources")

    with st.container(border=True):
        st.markdown("**E-REDES**")
        st.caption("Electricity consumption data")
        st.warning("Integration pending")

    with st.container(border=True):
        st.markdown("**Pordata**")
        st.caption("Territorial and socioeconomic indicators")
        st.warning("Integration pending")

with col2:
    st.markdown("#### Analytical Components")

    with st.container(border=True):
        st.markdown("**Data Integration**")
        st.caption("Data cleaning and harmonisation")
        st.warning("In development")

    with st.container(border=True):
        st.markdown("**Analytical Models**")
        st.caption("Statistical analysis and machine learning")
        st.info("Not available yet")

st.divider()

st.subheader("Recent Activity")
st.caption("Latest platform operations and updates.")

activities = [
    {
        "icon": "📁",
        "title": "E-REDES dataset registered",
        "description": "Electricity consumption data source added.",
        "date": "19 Nov 2026"
    },
    {
        "icon": "🔄",
        "title": "Data integration initiated",
        "description": "Preparing territorial data harmonisation.",
        "date": "18 Nov 2026"
    },
    {
        "icon": "📊",
        "title": "Statistical analysis completed",
        "description": "Descriptive analysis executed.",
        "date": "17 Nov 2026"
    },
]

for activity in activities:
    with st.container(border=True):
        col1, col2 = st.columns([0.12, 0.88])

        with col1:
            st.markdown(
                f"<div style='font-size: 1.5rem;'>{activity['icon']}</div>",
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(f"**{activity['title']}**")
            st.caption(activity["description"])
            st.caption(activity["date"])