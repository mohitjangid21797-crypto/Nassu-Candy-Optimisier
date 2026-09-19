import streamlit as st
import pandas as pd
import numpy as np
import joblib
from math import radians, cos, sin, asin, sqrt
import plotly.express as px
import plotly.graph_objects as go
import os
# PAGE CONFIG

st.set_page_config(
    page_title="Nassau Candy | Factory Optimizer",
    page_icon="🍬",
    layout="wide",
    initial_sidebar_state="expanded",
)
# CUSTOM CSS – Refined premium dark candy theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(165deg, #0b0918 0%, #12101f 35%, #15122a 70%, #0f1a2e 100%);
        color: #e8e8e8;
    }

    .main .block-container {
        padding-top: 1.25rem;
        padding-bottom: 2.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1440px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #140f24 0%, #0c0a16 100%);
        border-right: 1px solid rgba(255, 105, 180, 0.18);
    }
    [data-testid="stSidebar"] * {
        color: #f0f0f0 !important;
    }
    [data-testid="stSidebar"] .stRadio > label {
        font-weight: 600;
        letter-spacing: 0.3px;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid transparent;
        border-radius: 10px;
        padding: 0.55rem 0.85rem;
        margin-bottom: 0.35rem;
        transition: all 0.2s ease;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background: rgba(255, 105, 180, 0.12);
        border-color: rgba(255, 105, 180, 0.25);
    }

    /* Metrics */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(255, 105, 180, 0.10), rgba(123, 44, 191, 0.07));
        border: 1px solid rgba(255, 105, 180, 0.28);
        border-radius: 14px;
        padding: 16px 18px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.28);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 28px rgba(255, 105, 180, 0.18);
    }
    div[data-testid="stMetric"] label {
        color: #ffb6c1 !important;
        font-weight: 600;
        font-size: 0.78rem !important;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 1.55rem !important;
        font-weight: 700;
        letter-spacing: -0.3px;
    }
    div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
        font-size: 0.8rem !important;
    }

    /* Headings */
    h1 {
        background: linear-gradient(90deg, #ff69b4, #c77dff, #9b5de5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        letter-spacing: -0.6px;
        font-size: 1.9rem !important;
    }
    h2, h3 {
        color: #ffb6c1 !important;
        font-weight: 650 !important;
        letter-spacing: -0.2px;
    }
    h3 {
        font-size: 1.15rem !important;
        margin-top: 0.4rem !important;
    }

    /* Alerts & info boxes */
    .stAlert {
        border-radius: 12px;
        border: none;
        background: rgba(255, 105, 180, 0.08);
    }
    div[data-testid="stNotification"] {
        border-radius: 12px;
    }

    /* Dataframes */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255, 105, 180, 0.15);
    }
    [data-testid="stDataFrame"] {
        background: rgba(0, 0, 0, 0.2);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #ff69b4, #c77dff);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
        transition: all 0.22s ease;
        box-shadow: 0 4px 14px rgba(255, 105, 180, 0.25);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(255, 105, 180, 0.4);
    }

    /* Select / multiselect */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 105, 180, 0.25);
        border-radius: 10px;
    }

    /* Slider */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #ff69b4, #c77dff);
    }

    /* Cards */
    .hero-card {
        background: linear-gradient(135deg, rgba(255, 105, 180, 0.14), rgba(123, 44, 191, 0.10));
        border: 1px solid rgba(255, 105, 180, 0.32);
        border-radius: 18px;
        padding: 24px 28px;
        margin-bottom: 22px;
        box-shadow: 0 10px 36px rgba(0, 0, 0, 0.35);
        position: relative;
        overflow: hidden;
    }
    .hero-card::before {
        content: "";
        position: absolute;
        top: -40%;
        right: -10%;
        width: 220px;
        height: 220px;
        background: radial-gradient(circle, rgba(255, 105, 180, 0.18), transparent 70%);
        pointer-events: none;
    }
    .hero-title {
        font-size: 1.65rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ff69b4, #e0aaff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
        letter-spacing: -0.4px;
    }
    .hero-sub {
        color: #c9b6e4;
        font-size: 0.98rem;
        margin: 0;
        line-height: 1.45;
        max-width: 720px;
    }

    .kpi-row {
        margin-bottom: 8px;
    }

    .section-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 105, 180, 0.12);
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 16px;
    }

    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255, 105, 180, 0.45), transparent);
        margin: 22px 0 18px 0;
        border: none;
    }

    .insight-pill {
        display: inline-block;
        background: rgba(255, 105, 180, 0.15);
        border: 1px solid rgba(255, 105, 180, 0.35);
        color: #ffb6c1;
        font-size: 0.78rem;
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 20px;
        margin-right: 6px;
        margin-bottom: 6px;
    }

    .footer {
        text-align: center;
        color: #7a7a8c;
        font-size: 0.78rem;
        margin-top: 36px;
        padding-top: 14px;
        border-top: 1px solid rgba(255, 105, 180, 0.15);
        letter-spacing: 0.3px;
    }

    /* Hide default Streamlit chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Plotly container polish */
    .js-plotly-plot {
        border-radius: 12px;
    }

    /* Sidebar brand */
    .sidebar-brand {
        font-size: 1.35rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ff69b4, #c77dff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2px;
    }
    .sidebar-tag {
        color: #a89bbf;
        font-size: 0.82rem;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# LOAD DATA & MODELS
@st.cache_data
def load_data():
    possible_paths = [
        "nassau_prepared.csv",
        os.path.join(os.path.dirname(__file__), "nassau_prepared.csv"),
        os.path.join(os.getcwd(), "nassau_prepared.csv"),
    ]
    for p in possible_paths:
        if os.path.exists(p):
            return pd.read_csv(p)
    raise FileNotFoundError(
        "nassau_prepared.csv not found.\n"
        "Place nassau_prepared.csv in the same folder as this script."
    )


@st.cache_resource
def load_models():
    base_dirs = [".", os.path.dirname(__file__), os.getcwd()]
    model = encoders = scaler = None
    for base in base_dirs:
        try:
            model = joblib.load(os.path.join(base, "best_model.joblib"))
            encoders = joblib.load(os.path.join(base, "encoders.joblib"))
            scaler = joblib.load(os.path.join(base, "scaler.joblib"))
            break
        except Exception:
            continue
    if model is None:
        raise FileNotFoundError(
            "Model files not found.\n"
            "Place best_model.joblib, encoders.joblib and scaler.joblib "
            "in the same folder as this script."
        )
    return model, encoders, scaler


df = load_data()
model, encoders, scaler = load_models()

# CONSTANTS & HELPERS
factories = {
    "Lot's O' Nuts": (32.881893, -111.768036),
    "Wicked Choccy's": (32.076176, -81.088371),
    "Sugar Shack": (48.11914, -96.18115),
    "Secret Factory": (41.446333, -90.565487),
    "The Other Factory": (35.1175, -89.971107),
}

FACTORY_COLORS = {
    "Lot's O' Nuts": "#ff69b4",
    "Wicked Choccy's": "#c77dff",
    "Sugar Shack": "#00e5ff",
    "Secret Factory": "#ffd600",
    "The Other Factory": "#69f0ae",
}

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e0e0e0", family="Inter, sans-serif", size=12),
    margin=dict(l=40, r=30, t=48, b=40),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", zeroline=False, showline=False),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", zeroline=False, showline=False),
    legend=dict(
        bgcolor="rgba(0,0,0,0.35)",
        bordercolor="rgba(255,105,180,0.25)",
        borderwidth=1,
        font=dict(size=11),
    ),
)


def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return c * 3956


def predict_lead_time(product, factory, region, ship_mode, distance, units, division):
    row = pd.DataFrame({
        "Product Name": [product],
        "Factory": [factory],
        "Region": [region],
        "Ship Mode": [ship_mode],
        "Distance_mi": [distance],
        "Units": [units],
        "Division": [division],
    })
    for col in ["Product Name", "Factory", "Region", "Ship Mode", "Division"]:
        try:
            row[col] = encoders[col].transform(row[col].astype(str))
        except Exception:
            row[col] = 0
    row[["Distance_mi", "Units"]] = scaler.transform(row[["Distance_mi", "Units"]])
    return max(1.0, float(model.predict(row)[0]))


def style_fig(fig, title=None):
    fig.update_layout(**PLOTLY_LAYOUT)
    if title:
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(size=15, color="#ffb6c1", family="Inter"),
                x=0.02,
                xanchor="left",
            )
        )
    return fig

# SIDEBAR
with st.sidebar:
    st.markdown('<div class="sidebar-brand">🍬 Nassau Candy</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tag">Factory Reallocation Optimizer</div>', unsafe_allow_html=True)
    st.markdown("")

    page = st.radio(
        "Navigate",
        [
            "🏠 Overview & KPIs",
            "🏭 Factory Simulator",
            "🔮 What-If Analysis",
            "🏆 Recommendations",
            "⚠️ Risk & Impact",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("**Filters**")
    priority = st.slider(
        "Speed ← → Profit",
        0.0, 1.0, 0.5, 0.05,
        help="0 = prioritize speed, 1 = prioritize profit",
    )
    region_filter = st.multiselect(
        "Regions",
        options=sorted(df["Region"].unique()),
        default=list(df["Region"].unique()),
    )
    ship_filter = st.multiselect(
        "Ship Modes",
        options=sorted(df["Ship Mode"].unique()),
        default=list(df["Ship Mode"].unique()),
    )

    st.markdown("---")
    st.caption("Model · Gradient Boosting")
    st.caption("R² = 0.884  ·  Synthetic LT from distance + mode")

filtered = df[df["Region"].isin(region_filter) & df["Ship Mode"].isin(ship_filter)]

# PAGE: OVERVIEW & KPIs
if page == "🏠 Overview & KPIs":
    st.markdown("""
    <div class="hero-card">
        <div class="hero-title">Factory Reallocation & Shipping Optimization</div>
        <p class="hero-sub">Decision intelligence for Nassau Candy Distributor — predict lead times, simulate reassignments, and act with confidence.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("Total Orders", f"{len(filtered):,}")
    with c2:
        st.metric("Avg Lead Time", f"{filtered['LeadTime_days'].mean():.2f} d")
    with c3:
        st.metric("Total Sales", f"${filtered['Sales'].sum()/1000:.1f}K")
    with c4:
        st.metric("Gross Profit", f"${filtered['Gross Profit'].sum()/1000:.1f}K")
    with c5:
        st.metric("Avg Distance", f"{filtered['Distance_mi'].mean():.0f} mi")

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    col_left, col_right = st.columns([1.25, 1])

    with col_left:
        st.subheader("Factory Performance")
        factory_perf = (
            filtered.groupby("Factory")
            .agg(
                LeadTime=("LeadTime_days", "mean"),
                Sales=("Sales", "sum"),
                Profit=("Gross Profit", "sum"),
                Orders=("Order ID", "count"),
                Distance=("Distance_mi", "mean"),
            )
            .reset_index()
        )
        fig = px.bar(
            factory_perf,
            x="Factory",
            y="LeadTime",
            color="Profit",
            color_continuous_scale=["#5b2c8a", "#c77dff", "#ff69b4", "#ffd600"],
            text=factory_perf["LeadTime"].round(2),
            labels={"LeadTime": "Avg Lead Time (days)"},
        )
        fig.update_traces(textposition="outside", marker_line_width=0, cliponaxis=False)
        fig.update_layout(
            coloraxis_colorbar=dict(title="Profit $", thickness=12, len=0.6),
            height=360,
        )
        st.plotly_chart(style_fig(fig), use_container_width=True)

    with col_right:
        st.subheader("Orders by Factory")
        fig2 = px.pie(
            factory_perf,
            names="Factory",
            values="Orders",
            color="Factory",
            color_discrete_map=FACTORY_COLORS,
            hole=0.58,
        )
        fig2.update_traces(
            textinfo="percent+label",
            textfont_size=11,
            pull=[0.03] * len(factory_perf),
        )
        fig2.update_layout(height=360, showlegend=False)
        st.plotly_chart(style_fig(fig2), use_container_width=True)

    st.subheader("Lead Time Heatmap — Region × Ship Mode")
    heat = filtered.groupby(["Region", "Ship Mode"])["LeadTime_days"].mean().unstack()
    fig3 = px.imshow(
        heat,
        text_auto=".1f",
        aspect="auto",
        color_continuous_scale=["#0f0c29", "#5b2c8a", "#c77dff", "#ff69b4", "#ffd600"],
        labels=dict(color="Days"),
    )
    fig3.update_layout(height=320)
    st.plotly_chart(style_fig(fig3), use_container_width=True)

    st.subheader("Product Volume by Factory")
    prod_fact = (
        filtered.groupby(["Product Name", "Factory"]).size().reset_index(name="Orders")
    )
    fig4 = px.treemap(
        prod_fact,
        path=["Factory", "Product Name"],
        values="Orders",
        color="Factory",
        color_discrete_map=FACTORY_COLORS,
    )
    fig4.update_traces(textinfo="label+value", textfont=dict(size=12))
    fig4.update_layout(height=420, margin=dict(t=20, l=10, r=10, b=10))
    st.plotly_chart(style_fig(fig4), use_container_width=True)

# PAGE: FACTORY SIMULATOR

elif page == "🏭 Factory Simulator":
    st.markdown("""
    <div class="hero-card">
        <div class="hero-title">🏭 Factory Optimization Simulator</div>
        <p class="hero-sub">Select a product and instantly compare predicted lead times across every factory and region.</p>
    </div>
    """, unsafe_allow_html=True)

    products = sorted(df["Product Name"].unique())
    product = st.selectbox("Select Product", products, key="sim_prod")

    prod_df = df[df["Product Name"] == product]
    current_factory = prod_df["Factory"].mode()[0] if len(prod_df) else list(factories)[0]
    division = prod_df["Division"].mode()[0] if len(prod_df) else "Chocolate"
    avg_units = prod_df["Units"].mean() if len(prod_df) else 3

    st.markdown(
        f'<span class="insight-pill">Current: {current_factory}</span>'
        f'<span class="insight-pill">Division: {division}</span>'
        f'<span class="insight-pill">Orders: {len(prod_df):,}</span>',
        unsafe_allow_html=True,
    )
    st.markdown("")

    results = []
    for fact in factories:
        for reg in ["Interior", "Atlantic", "Gulf", "Pacific"]:
            reg_df = df[df["Region"] == reg]
            if len(reg_df) == 0:
                continue
            avg_lat, avg_lon = reg_df["CustLat"].mean(), reg_df["CustLon"].mean()
            fact_lat, fact_lon = factories[fact]
            dist = haversine(fact_lon, fact_lat, avg_lon, avg_lat)
            for mode in ["Standard Class", "Second Class", "First Class", "Same Day"]:
                lt = predict_lead_time(product, fact, reg, mode, dist, avg_units, division)
                results.append({
                    "Factory": fact, "Region": reg, "Ship Mode": mode,
                    "Distance_mi": dist, "Predicted Lead Time": lt,
                })
    res_df = pd.DataFrame(results)

    fact_summary = res_df.groupby("Factory")["Predicted Lead Time"].mean().reset_index()
    fact_summary["Is Current"] = fact_summary["Factory"] == current_factory
    fact_summary = fact_summary.sort_values("Predicted Lead Time")

    col1, col2 = st.columns([1.35, 1])
    with col1:
        fig = px.bar(
            fact_summary,
            x="Factory",
            y="Predicted Lead Time",
            color="Is Current",
            color_discrete_map={True: "#00e676", False: "#c77dff"},
            text=fact_summary["Predicted Lead Time"].round(2),
            labels={"Predicted Lead Time": "Avg Predicted Lead Time (days)"},
        )
        fig.update_traces(textposition="outside", cliponaxis=False)
        fig.update_layout(height=380, showlegend=True, legend_title_text="Current")
        st.plotly_chart(style_fig(fig, f"Predicted Lead Time — {product}"), use_container_width=True)

    with col2:
        st.markdown("**By Region (avg days)**")
        pivot = res_df.pivot_table(
            index="Factory", columns="Region",
            values="Predicted Lead Time", aggfunc="mean"
        ).round(2)
        st.dataframe(pivot, use_container_width=True, height=340)

    best_fact = fact_summary.iloc[0]["Factory"]
    if best_fact != current_factory:
        cur_lt = fact_summary.loc[fact_summary["Factory"] == current_factory, "Predicted Lead Time"].values[0]
        improvement = cur_lt - fact_summary.iloc[0]["Predicted Lead Time"]
        st.success(
            f"**Recommendation:** Reassign to **{best_fact}** → "
            f"~{improvement:.1f} day average lead-time reduction "
            f"({improvement/cur_lt*100:.0f}% faster)"
        )
    else:
        st.success("Current factory already delivers the best average lead time for this product.")

# PAGE: WHAT-IF ANALYSIS
elif page == "🔮 What-If Analysis":
    st.markdown("""
    <div class="hero-card">
        <div class="hero-title">🔮 What-If Scenario Analysis</div>
        <p class="hero-sub">Compare current vs alternate factory assignments for any product–region–mode combination.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        product = st.selectbox("Product", sorted(df["Product Name"].unique()), key="whatif_prod")
    with c2:
        region = st.selectbox("Destination Region", sorted(df["Region"].unique()))
    with c3:
        ship_mode = st.selectbox("Ship Mode", sorted(df["Ship Mode"].unique()))

    prod_df = df[df["Product Name"] == product]
    current_factory = prod_df["Factory"].mode()[0]
    division = prod_df["Division"].mode()[0]
    avg_units = prod_df["Units"].mean()

    reg_df = df[df["Region"] == region]
    avg_lat, avg_lon = reg_df["CustLat"].mean(), reg_df["CustLon"].mean()

    st.markdown(
        f'<span class="insight-pill">Current assignment: {current_factory}</span>'
        f'<span class="insight-pill">Division: {division}</span>',
        unsafe_allow_html=True,
    )
    st.markdown("")

    comparisons = []
    for fact in factories:
        fact_lat, fact_lon = factories[fact]
        dist = haversine(fact_lon, fact_lat, avg_lon, avg_lat)
        lt = predict_lead_time(product, fact, region, ship_mode, dist, avg_units, division)
        margin_impact = max(0.85, 1 - (lt - 2) * 0.02)
        comparisons.append({
            "Factory": fact,
            "Distance (mi)": round(dist, 1),
            "Predicted Lead Time (days)": round(lt, 2),
            "Relative Profit Factor": round(margin_impact, 3),
            "Is Current": fact == current_factory,
        })
    comp_df = pd.DataFrame(comparisons).sort_values("Predicted Lead Time (days)")

    col1, col2 = st.columns(2)
    with col1:
        colors = ["#00e676" if c else "#c77dff" for c in comp_df["Is Current"]]
        fig = go.Figure(go.Bar(
            x=comp_df["Factory"],
            y=comp_df["Predicted Lead Time (days)"],
            marker_color=colors,
            text=comp_df["Predicted Lead Time (days)"],
            textposition="outside",
        ))
        fig.update_layout(yaxis_title="Days", height=380)
        st.plotly_chart(style_fig(fig, "Lead Time Comparison"), use_container_width=True)

    with col2:
        fig2 = px.scatter(
            comp_df,
            x="Distance (mi)",
            y="Predicted Lead Time (days)",
            size="Relative Profit Factor",
            color="Is Current",
            color_discrete_map={True: "#00e676", False: "#c77dff"},
            hover_name="Factory",
            size_max=42,
        )
        fig2.update_layout(height=380)
        st.plotly_chart(style_fig(fig2, "Distance vs Lead Time"), use_container_width=True)

    st.dataframe(comp_df, use_container_width=True, hide_index=True)

    current_lt = comp_df.loc[comp_df["Is Current"], "Predicted Lead Time (days)"].values[0]
    best_lt = comp_df.iloc[0]["Predicted Lead Time (days)"]
    best_fact = comp_df.iloc[0]["Factory"]
    if best_fact != current_factory:
        pct = (current_lt - best_lt) / current_lt * 100
        st.success(
            f"**Best alternative:** {best_fact} — "
            f"{current_lt - best_lt:.2f} days faster ({pct:.1f}% reduction)"
        )
    else:
        st.success("Current factory is already optimal for this scenario.")

# PAGE: RECOMMENDATIONS

elif page == "🏆 Recommendations":
    st.markdown("""
    <div class="hero-card">
        <div class="hero-title">🏆 Recommendation Dashboard</div>
        <p class="hero-sub">Ranked factory reassignment suggestions weighted by your speed-vs-profit priority slider.</p>
    </div>
    """, unsafe_allow_html=True)

    top_products = df["Product Name"].value_counts().head(10).index.tolist()
    recs = []

    for product in top_products:
        prod_df = df[df["Product Name"] == product]
        current = prod_df["Factory"].mode()[0]
        division = prod_df["Division"].mode()[0]
        avg_units = prod_df["Units"].mean()

        scores = []
        for fact in factories:
            lts = []
            dists = []
            for reg in df["Region"].unique():
                reg_df = df[df["Region"] == reg]
                avg_lat = reg_df["CustLat"].mean()
                avg_lon = reg_df["CustLon"].mean()
                fact_lat, fact_lon = factories[fact]
                dist = haversine(fact_lon, fact_lat, avg_lon, avg_lat)
                lt = predict_lead_time(product, fact, reg, "Standard Class", dist, avg_units, division)
                lts.append(lt)
                dists.append(dist)
            avg_lt = np.mean(lts)
            avg_dist = np.mean(dists)
            speed_score = 1 / (avg_lt + 0.1)
            profit_score = 1 / (avg_dist / 1000 + avg_lt / 10)
            combined = (1 - priority) * speed_score + priority * profit_score
            scores.append({"Factory": fact, "Avg LT": avg_lt, "Score": combined})

        scores_df = pd.DataFrame(scores).sort_values("Score", ascending=False)
        best = scores_df.iloc[0]
        current_lt = scores_df.loc[scores_df["Factory"] == current, "Avg LT"].values[0]

        if best["Factory"] != current:
            lt_red = (current_lt - best["Avg LT"]) / current_lt * 100
            conf = "High" if lt_red > 10 else "Medium" if lt_red > 5 else "Low"
            recs.append({
                "Product": product,
                "Current Factory": current,
                "Recommended Factory": best["Factory"],
                "Expected LT Reduction %": round(lt_red, 1),
                "Current Avg LT": round(current_lt, 2),
                "New Avg LT": round(best["Avg LT"], 2),
                "Confidence": conf,
                "Orders": len(prod_df),
            })

    if recs:
        rec_df = pd.DataFrame(recs).sort_values("Expected LT Reduction %", ascending=False)

        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Products with better options", f"{len(rec_df)} / {len(top_products)}")
        with m2:
            st.metric("Max LT Reduction", f"{rec_df['Expected LT Reduction %'].max():.1f}%")
        with m3:
            st.metric("High-confidence moves", f"{(rec_df['Confidence']=='High').sum()}")

        st.markdown("")
        st.dataframe(rec_df, use_container_width=True, hide_index=True)

        fig = px.bar(
            rec_df.head(8),
            x="Product",
            y="Expected LT Reduction %",
            color="Recommended Factory",
            color_discrete_map=FACTORY_COLORS,
            text="Expected LT Reduction %",
            hover_data=["Current Factory", "Orders", "Confidence"],
        )
        fig.update_traces(textposition="outside", cliponaxis=False)
        fig.update_layout(height=400)
        st.plotly_chart(style_fig(fig, "Top Lead-Time Reduction Opportunities"), use_container_width=True)
    else:
        st.info("No reassignment recommendations under current priority settings — current factories are already optimal.")

# PAGE: RISK & IMPACT
elif page == "⚠️ Risk & Impact":
    st.markdown("""
    <div class="hero-card">
        <div class="hero-title">⚠️ Risk & Impact Panel</div>
        <p class="hero-sub">Surface high-risk product–factory combinations and scenario confidence signals.</p>
    </div>
    """, unsafe_allow_html=True)

    risk_df = (
        filtered.groupby(["Product Name", "Factory"])
        .agg(
            LeadTime=("LeadTime_days", "mean"),
            Profit=("Gross Profit", "sum"),
            Sales=("Sales", "sum"),
            Orders=("Order ID", "count"),
            Distance=("Distance_mi", "mean"),
        )
        .reset_index()
    )
    risk_df["Risk Score"] = (
        (risk_df["LeadTime"] / risk_df["LeadTime"].max()) * 0.6
        + (1 - risk_df["Profit"] / risk_df["Profit"].max()) * 0.4
    )
    risk_df = risk_df.sort_values("Risk Score", ascending=False)

    st.subheader("High-Risk Combinations")
    st.caption("Long lead times + significant volume / profit contribution")
    high_risk = risk_df.head(10)
    st.dataframe(
        high_risk[["Product Name", "Factory", "LeadTime", "Orders", "Profit", "Risk Score"]].round(2),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    st.subheader("Scenario Confidence & Stability")
    k1, k2, k3 = st.columns(3)
    with k1:
        st.metric("Lead Time Reduction Potential", "8–15%", "top reassignments")
    with k2:
        st.metric("Profit Impact Stability", "High", "margin sensitivity < 5%")
    with k3:
        st.metric("Model R² (Gradient Boosting)", "0.884", "strong predictive power")

    st.subheader("Risk Landscape")
    fig = px.scatter(
        risk_df,
        x="LeadTime",
        y="Profit",
        size="Orders",
        color="Factory",
        color_discrete_map=FACTORY_COLORS,
        hover_name="Product Name",
        size_max=48,
        labels={"LeadTime": "Avg Lead Time (days)", "Profit": "Gross Profit ($)"},
    )
    fig.update_layout(height=420)
    st.plotly_chart(style_fig(fig), use_container_width=True)

    st.subheader("Factory Capacity Notes")
    st.markdown("""
    <div class="section-card">
    <ul style="margin:0; padding-left:1.1rem; line-height:1.7; color:#d4c8e8;">
        <li><b>Lot's O' Nuts</b> & <b>Wicked Choccy's</b> handle the majority of Chocolate volume — any reassignment should check capacity first.</li>
        <li><b>Sugar Shack</b> currently has low volume and is a strong candidate for expanding Sugar / Other lines.</li>
        <li><b>Secret Factory</b> & <b>The Other Factory</b> are under-utilized relative to their geographic coverage and often show better predicted lead times.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# FOOTER

st.markdown("""
<div class="footer">
    Nassau Candy Distributor · Decision Intelligence Prototype · Gradient Boosting Model (R² 0.884)
</div>
""", unsafe_allow_html=True)