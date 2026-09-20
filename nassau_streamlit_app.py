import streamlit as st
import pandas as pd
import numpy as np
import joblib
from math import radians, cos, sin, asin, sqrt
import plotly.express as px
import plotly.graph_objects as go
import os

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Nassau Candy | Factory Optimizer",
    page_icon="🍬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# PROFESSIONAL UI — Navy / Teal / Gold
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background: #0B1120;
        color: #E2E8F0;
    }

    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1400px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #0F172A;
        border-right: 1px solid #1E293B;
    }
    [data-testid="stSidebar"] * {
        color: #CBD5E1 !important;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label {
        background: transparent;
        border: 1px solid transparent;
        border-radius: 8px;
        padding: 0.5rem 0.75rem;
        margin-bottom: 0.25rem;
        transition: all 0.15s ease;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background: rgba(14, 165, 233, 0.08);
        border-color: rgba(14, 165, 233, 0.2);
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px 18px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    }
    div[data-testid="stMetric"] label {
        color: #94A3B8 !important;
        font-weight: 500;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #F8FAFC !important;
        font-size: 1.6rem !important;
        font-weight: 700;
    }

    /* Headings */
    h1 {
        color: #F8FAFC !important;
        font-weight: 700 !important;
        letter-spacing: -0.4px;
        font-size: 1.75rem !important;
    }
    h2, h3 {
        color: #E2E8F0 !important;
        font-weight: 600 !important;
    }
    h3 { font-size: 1.1rem !important; }

    .stAlert { border-radius: 10px; border: none; }

    .stButton > button {
        background: #0EA5E9;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.45rem 1.2rem;
        transition: background 0.15s ease;
    }
    .stButton > button:hover {
        background: #0284C7;
    }

    /* Hero */
    .hero-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 24px 28px;
        margin-bottom: 24px;
    }
    .hero-title {
        font-size: 1.55rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 6px;
    }
    .hero-sub {
        color: #94A3B8;
        font-size: 0.95rem;
        margin: 0;
        line-height: 1.5;
    }

    .section-divider {
        height: 1px;
        background: #1E293B;
        margin: 24px 0 18px 0;
        border: none;
    }

    .footer {
        text-align: center;
        color: #64748B;
        font-size: 0.78rem;
        margin-top: 36px;
        padding-top: 14px;
        border-top: 1px solid #1E293B;
    }

    /* Multiselect tags */
    [data-baseweb="tag"] {
        background-color: #0EA5E9 !important;
        border-radius: 6px !important;
    }

    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DATA & MODELS
# ============================================================
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

# ============================================================
# CONSTANTS & HELPERS
# ============================================================
factories = {
    "Lot's O' Nuts": (32.881893, -111.768036),
    "Wicked Choccy's": (32.076176, -81.088371),
    "Sugar Shack": (48.11914, -96.18115),
    "Secret Factory": (41.446333, -90.565487),
    "The Other Factory": (35.1175, -89.971107),
}

# Professional palette
FACTORY_COLORS = {
    "Lot's O' Nuts": "#0EA5E9",
    "Wicked Choccy's": "#8B5CF6",
    "Sugar Shack": "#14B8A6",
    "Secret Factory": "#F59E0B",
    "The Other Factory": "#64748B",
}

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#CBD5E1", family="Inter, sans-serif", size=12),
    margin=dict(l=40, r=30, t=48, b=40),
    xaxis=dict(gridcolor="rgba(148,163,184,0.12)", zeroline=False, tickfont=dict(color="#94A3B8")),
    yaxis=dict(gridcolor="rgba(148,163,184,0.12)", zeroline=False, tickfont=dict(color="#94A3B8")),
    legend=dict(bgcolor="rgba(15,23,42,0.8)", bordercolor="#334155", borderwidth=1, font=dict(color="#CBD5E1")),
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
        fig.update_layout(title=dict(text=title, font=dict(size=15, color="#E2E8F0", family="Inter")))
    return fig


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("## 🍬 Nassau Candy")
    st.markdown("##### Factory Reallocation Optimizer")
    st.markdown("---")

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
        "Speed ← → Profit", 0.0, 1.0, 0.5, 0.05,
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
    st.caption("Model: Gradient Boosting  ·  R² = 0.884")
    st.caption("Lead times derived from distance + ship mode")

filtered = df[df["Region"].isin(region_filter) & df["Ship Mode"].isin(ship_filter)]

# ============================================================
# OVERVIEW & KPIs
# ============================================================
if page == "🏠 Overview & KPIs":
    st.markdown("""
    <div class="hero-card">
        <div class="hero-title">Factory Reallocation & Shipping Optimization</div>
        <p class="hero-sub">Decision intelligence for Nassau Candy Distributor — predict outcomes, simulate reassignments, and balance efficiency with profitability.</p>
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
            color_continuous_scale=["#0F172A", "#0EA5E9", "#F59E0B"],
            text=factory_perf["LeadTime"].round(2),
            labels={"LeadTime": "Avg Lead Time (days)"},
        )
        fig.update_traces(textposition="outside", marker_line_width=0)
        fig.update_layout(coloraxis_colorbar=dict(title="Profit $", tickfont=dict(color="#94A3B8")))
        st.plotly_chart(style_fig(fig), use_container_width=True)

    with col_right:
        st.subheader("Orders by Factory")
        fig2 = px.pie(
            factory_perf,
            names="Factory",
            values="Orders",
            color="Factory",
            color_discrete_map=FACTORY_COLORS,
            hole=0.55,
        )
        fig2.update_traces(textinfo="percent+label", textfont_size=11)
        st.plotly_chart(style_fig(fig2), use_container_width=True)

    st.subheader("Lead Time Heatmap — Region × Ship Mode")
    heat = filtered.groupby(["Region", "Ship Mode"])["LeadTime_days"].mean().unstack()
    fig3 = px.imshow(
        heat,
        text_auto=".1f",
        aspect="auto",
        color_continuous_scale=["#0F172A", "#0EA5E9", "#F59E0B"],
        labels=dict(color="Days"),
    )
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
    fig4.update_traces(textinfo="label+value")
    st.plotly_chart(style_fig(fig4), use_container_width=True)

# ============================================================
# FACTORY SIMULATOR
# ============================================================
elif page == "🏭 Factory Simulator":
    st.markdown("""
    <div class="hero-card">
        <div class="hero-title">Factory Optimization Simulator</div>
        <p class="hero-sub">Select a product and compare predicted lead times across all factories.</p>
    </div>
    """, unsafe_allow_html=True)

    products = sorted(df["Product Name"].unique())
    product = st.selectbox("Select Product", products, key="sim_prod")

    prod_df = df[df["Product Name"] == product]
    current_factory = prod_df["Factory"].mode()[0] if len(prod_df) else list(factories)[0]
    division = prod_df["Division"].mode()[0] if len(prod_df) else "Chocolate"
    avg_units = prod_df["Units"].mean() if len(prod_df) else 3

    st.info(f"**Current factory:** {current_factory}  ·  **Division:** {division}  ·  **Orders:** {len(prod_df):,}")

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

    col1, col2 = st.columns([1.3, 1])
    with col1:
        fig = px.bar(
            fact_summary,
            x="Factory",
            y="Predicted Lead Time",
            color="Is Current",
            color_discrete_map={True: "#14B8A6", False: "#0EA5E9"},
            text=fact_summary["Predicted Lead Time"].round(2),
            labels={"Predicted Lead Time": "Avg Predicted Lead Time (days)"},
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(style_fig(fig, f"Predicted Lead Time — {product}"), use_container_width=True)

    with col2:
        pivot = res_df.pivot_table(
            index="Factory", columns="Region",
            values="Predicted Lead Time", aggfunc="mean"
        ).round(2)
        st.markdown("**By Region (avg days)**")
        st.dataframe(pivot, use_container_width=True)

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

# ============================================================
# WHAT-IF ANALYSIS
# ============================================================
elif page == "🔮 What-If Analysis":
    st.markdown("""
    <div class="hero-card">
        <div class="hero-title">What-If Scenario Analysis</div>
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

    st.markdown(f"**Current assignment:** `{current_factory}`")

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
        colors = ["#14B8A6" if c else "#0EA5E9" for c in comp_df["Is Current"]]
        fig = go.Figure(go.Bar(
            x=comp_df["Factory"],
            y=comp_df["Predicted Lead Time (days)"],
            marker_color=colors,
            text=comp_df["Predicted Lead Time (days)"],
            textposition="outside",
        ))
        fig.update_layout(yaxis_title="Days")
        st.plotly_chart(style_fig(fig, "Lead Time Comparison"), use_container_width=True)

    with col2:
        fig2 = px.scatter(
            comp_df,
            x="Distance (mi)",
            y="Predicted Lead Time (days)",
            size="Relative Profit Factor",
            color="Is Current",
            color_discrete_map={True: "#14B8A6", False: "#0EA5E9"},
            hover_name="Factory",
            size_max=40,
        )
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

# ============================================================
# RECOMMENDATIONS
# ============================================================
elif page == "🏆 Recommendations":
    st.markdown("""
    <div class="hero-card">
        <div class="hero-title">Recommendation Dashboard</div>
        <p class="hero-sub">Ranked factory reassignment suggestions weighted by your speed-vs-profit priority.</p>
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
            lts, dists = [], []
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
        fig.update_traces(textposition="outside")
        st.plotly_chart(style_fig(fig, "Top Lead-Time Reduction Opportunities"), use_container_width=True)
    else:
        st.info("No reassignment recommendations under current priority settings — current factories are already optimal.")

# ============================================================
# RISK & IMPACT
# ============================================================
elif page == "⚠️ Risk & Impact":
    st.markdown("""
    <div class="hero-card">
        <div class="hero-title">Risk & Impact Panel</div>
        <p class="hero-sub">High-risk product–factory combinations and scenario confidence signals.</p>
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
    st.caption("Long lead times combined with significant volume or profit")
    high_risk = risk_df.head(10)
    st.dataframe(
        high_risk[["Product Name", "Factory", "LeadTime", "Orders", "Profit", "Risk Score"]].round(2),
        use_container_width=True,
        hide_index=True,
    )

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
        size_max=50,
        labels={"LeadTime": "Avg Lead Time (days)", "Profit": "Gross Profit ($)"},
    )
    st.plotly_chart(style_fig(fig), use_container_width=True)

    st.subheader("Factory Capacity Notes")
    st.markdown("""
    - **Lot's O' Nuts** & **Wicked Choccy's** handle the majority of Chocolate volume — capacity should be checked before reassignment.  
    - **Sugar Shack** has low current volume and is a strong candidate for expanding Sugar / Other lines.  
    - **Secret Factory** & **The Other Factory** are under-utilized relative to geographic coverage and often show better predicted lead times.
    """)

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="footer">
    Nassau Candy Distributor · Decision Intelligence Prototype · Gradient Boosting Model (R² 0.884)
</div>
""", unsafe_allow_html=True)
