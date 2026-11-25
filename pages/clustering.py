
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


######### Dados ficticios 
import numpy as np

# Temporary Mock Data
np.random.seed(42)

cluster_data = pd.DataFrame({
    "Territory": [
        "Guarda", "Covilhã", "Lisboa", "Porto",
        "Braga", "Aveiro", "Coimbra", "Viseu",
        "Faro", "Leiria", "Évora", "Beja",
        "Setúbal", "Viana do Castelo", "Vila Real",
        "Bragança", "Santarém", "Castelo Branco"
    ],
    "Energy Consumption": np.random.randint(200, 900, 18),
    "Economic Activity": np.random.randint(100, 800, 18),
    "Cluster": np.random.choice(
        ["Cluster 1", "Cluster 2", "Cluster 3"], 18
    )
})

########

# Page Header
st.title("Clustering")
st.caption(
    "Explore territorial patterns through "
    "unsupervised machine learning."
)

st.divider()

# Clustering Configuration
st.subheader("Clustering Configuration")
st.caption("Configure the parameters for the clustering analysis.")

col1, col2 = st.columns(2)

with col1:
    algorithm = st.selectbox(
        "Clustering Algorithm",
        ["K-Means", "Hierarchical Clustering", "DBSCAN"]
    )

with col2:
    normalization = st.selectbox(
        "Normalization Method",
        ["StandardScaler", "MinMaxScaler", "RobustScaler", "None"]
    )

col1, col2 = st.columns(2)

with col1:
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

with col2:
    distance_metric = st.selectbox(
        "Distance Metric",
        ["Euclidean", "Manhattan", "Cosine"]
    )

st.markdown("#### Input Indicators")

indicators = st.multiselect(
    "Select indicators for clustering",
    [
        "Energy Consumption",
        "Population Density",
        "Economic Activity",
        "Renewable Energy Production"
    ],
    default=[
        "Energy Consumption",
        "Population Density"
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

## st.divider()

st.markdown("#### Algorithm Parameters")

if algorithm == "K-Means":

    col1, col2 = st.columns(2)

    with col1:
        n_clusters = st.slider(
            "Number of Clusters (K)",
            min_value=2,
            max_value=10,
            value=3
        )

    with col2:
        max_iterations = st.slider(
            "Maximum Iterations",
            min_value=100,
            max_value=1000,
            value=300,
            step=100
        )

elif algorithm == "Hierarchical Clustering":

    col1, col2 = st.columns(2)

    with col1:
        n_clusters = st.slider(
            "Number of Clusters",
            min_value=2,
            max_value=10,
            value=3
        )

    with col2:
        linkage_method = st.selectbox(
            "Linkage Method",
            ["Ward", "Complete", "Average", "Single"]
        )

elif algorithm == "DBSCAN":

    col1, col2 = st.columns(2)

    with col1:
        eps = st.slider(
            "Epsilon (Neighborhood Radius)",
            min_value=0.1,
            max_value=5.0,
            value=0.5,
            step=0.1
        )

    with col2:
        min_samples = st.slider(
            "Minimum Samples",
            min_value=2,
            max_value=20,
            value=5
        )

st.divider()

col1, col2 = st.columns([3, 1])

with col1:
    st.caption(
        "Run the clustering process using the selected configuration."
    )

with col2:
    run_clustering = st.button(
        "Run Clustering",
        type="primary",
        use_container_width=True
    )

if run_clustering:
    if len(indicators) < 2:
        st.warning("Select at least two indicators.")
    elif start_year > end_year:
        st.warning("Invalid time period.")
    else:
        st.info(
            "Configuration validated. "
            "Clustering execution will be connected to the analytics service."
        )

#### EXECUÇÃO

st.divider()
st.subheader("Cluster Overview")
st.caption("Summary of the clustering results.")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Clusters",
        value="3"
    )

with col2:
    st.metric(
        label="Territories Analysed",
        value="18"
    )

with col3:
    st.metric(
        label="Average Cluster Size",
        value="6"
    )

with col4:
    st.metric(
        label="Silhouette Score",
        value="0.74"
    )

st.divider()
st.subheader("Cluster Visualisation")
st.caption("Explore the distribution of territories across identified clusters.")

col1, col2 = st.columns(2)

with col1:
    x_axis = st.selectbox(
        "X Axis",
        ["Energy Consumption", "Economic Activity"],
        key="cluster_x"
    )

with col2:
    y_axis = st.selectbox(
        "Y Axis",
        ["Economic Activity", "Energy Consumption"],
        key="cluster_y"
    )

fig_clusters = px.scatter(
    cluster_data,
    x=x_axis,
    y=y_axis,
    color="Cluster",
    text="Territory",
    color_discrete_sequence=[
        "#00B8D9",
        "#7955D9",
        "#B87948"
    ]
)

fig_clusters.update_traces(
    marker=dict(size=13, line=dict(width=1, color="#FFFFFF")),
    textposition="top center"
)

fig_clusters.update_layout(
    template=plotly_template,
    height=500,
    paper_bgcolor=paper_color,
    plot_bgcolor=plot_color,
    font=dict(color=text_color),
    margin=dict(l=20, r=20, t=30, b=20),
    xaxis=dict(showgrid=True, gridcolor=grid_color),
    yaxis=dict(showgrid=True, gridcolor=grid_color),
    legend_title_text="Cluster"
)

st.plotly_chart(fig_clusters, use_container_width=True)

st.divider()
st.subheader("Cluster Characteristics")
st.caption("Compare the average indicator values across identified clusters.")

cluster_profile = (
    cluster_data
    .groupby("Cluster")[
        ["Energy Consumption", "Economic Activity"]
    ]
    .mean()
    .reset_index()
)

fig_profile = px.bar(
    cluster_profile.melt(
        id_vars="Cluster",
        var_name="Indicator",
        value_name="Average Value"
    ),
    x="Cluster",
    y="Average Value",
    color="Indicator",
    barmode="group",
    color_discrete_sequence=["#00B8D9", "#7955D9"]
)

fig_profile.update_layout(
    template=plotly_template,
    height=400,
    paper_bgcolor=paper_color,
    plot_bgcolor=plot_color,
    font=dict(color=text_color),
    margin=dict(l=20, r=20, t=20, b=20),
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor=grid_color)
)

st.plotly_chart(fig_profile, use_container_width=True)


st.markdown("#### Cluster Summary")

st.dataframe(
    cluster_profile,
    use_container_width=True,
    hide_index=True
)


st.divider()
st.subheader("Territorial Distribution")
st.caption(
    "Explore the geographical distribution of territories "
    "across the identified clusters."
)

st.info(
    "Geographical visualisation will be available "
    "once territorial boundary data is integrated."
)

st.divider()
st.subheader("Cluster Insights")
st.caption("Key observations about the identified territorial groups.")

col1, col2 = st.columns(2)

with col1:
    st.info(
        "**Cluster 1**\n\n"
        "This group represents territories with a distinct "
        "combination of energy consumption and economic activity."
    )

with col2:
    st.info(
        "**Cluster 2 & 3**\n\n"
        "These groups represent different territorial profiles "
        "based on the selected indicators."
    )


st.divider()
st.subheader("Export Analysis")
st.caption("Download clustering results for further analysis.")

col1, col2 = st.columns(2)

with col1:
    st.download_button(
        label="Cluster Assignments",
        data=cluster_data.to_csv(index=False).encode("utf-8"),
        file_name="cluster_assignments.csv",
        mime="text/csv",
        use_container_width=True
    )

with col2:
    st.download_button(
        label="Cluster Summary",
        data=cluster_profile.to_csv(index=False).encode("utf-8"),
        file_name="cluster_summary.csv",
        mime="text/csv",
        use_container_width=True
    )