"""
app.py — Diagnostic Lab Operational Analytics Dashboard
=========================================================
A locally-runnable Streamlit app that visualises sample logistics and
lab operations metrics for diagnostic labs.

Run with:
    streamlit run app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ── Make sure utils/ is importable regardless of CWD ──────────────────────
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.data_loader import get_journey_df
from utils import metrics as m

# ═══════════════════════════════════════════════════════════════════════════
# Page config
# ═══════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Lab Ops Analytics Dashboard",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════════
# Global CSS — clean B2B look
# ═══════════════════════════════════════════════════════════════════════════
st.markdown(
    """
    <style>
        /* Import Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

        /* Sidebar branding strip */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        }
        section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
        section[data-testid="stSidebar"] .stMarkdown h2 {
            color: #38bdf8 !important; font-size: 1.05rem; letter-spacing: 0.05em;
        }

        /* Hide default top margin */
        .block-container { padding-top: 1.5rem; }

        /* KPI card style */
        .kpi-card {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 18px 22px;
            text-align: center;
            color: #f1f5f9;
        }
        .kpi-label  { font-size: 0.78rem; color: #94a3b8; text-transform: uppercase;
                      letter-spacing: 0.06em; margin-bottom: 6px; }
        .kpi-value  { font-size: 2rem; font-weight: 700; color: #38bdf8; line-height: 1.1; }
        .kpi-sub    { font-size: 0.75rem; color: #64748b; margin-top: 4px; }

        /* Section headers */
        .section-title {
            font-size: 1.1rem; font-weight: 600; color: #2563EB;
            border-left: 4px solid #38bdf8; padding-left: 10px;
            margin: 24px 0 12px 0;
        }

        /* Tab styling override */
        .stTabs [data-baseweb="tab-list"] { gap: 6px; }
        .stTabs [data-baseweb="tab"] {
            font-size: 0.85rem; font-weight: 500;
            padding: 8px 18px; border-radius: 8px 8px 0 0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ═══════════════════════════════════════════════════════════════════════════
# Load data (cached across reruns via Streamlit cache)
# ═══════════════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner="Loading data …")
def load_data() -> pd.DataFrame:
    return get_journey_df()


df_full = load_data()

# ═══════════════════════════════════════════════════════════════════════════
# Sidebar — Global Filters
# ═══════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🧪 Lab Ops Dashboard")
    st.caption("Diagnostic Lab Operational Analytics")
    st.divider()

    # Date range
    min_date = df_full["collection_date"].min()
    max_date = df_full["collection_date"].max()
    date_range = st.date_input(
        "📅 Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    st.divider()

    # City
    cities = sorted(df_full["city"].dropna().unique().tolist())
    sel_cities = st.multiselect("🏙 City", cities, default=cities)

    # Lab
    labs = sorted(df_full["lab_name"].dropna().unique().tolist())
    sel_labs = st.multiselect("🏥 Lab", labs, default=labs)

    # Courier
    couriers = sorted(df_full["courier_name"].dropna().unique().tolist())
    sel_couriers = st.multiselect("🚚 Courier", couriers, default=couriers)

    # Test type
    tests = sorted(df_full["test_name"].dropna().unique().tolist())
    sel_tests = st.multiselect("🔬 Test Type", tests, default=tests)

    # Sample status
    statuses = sorted(df_full["sample_status"].dropna().unique().tolist())
    sel_statuses = st.multiselect("📊 Sample Status", statuses, default=statuses)

    st.divider()
    st.caption("Data: synthetic · No cloud required")

# ── Apply filters ──────────────────────────────────────────────────────────
try:
    d_start, d_end = date_range[0], date_range[1]
except (IndexError, TypeError):
    d_start, d_end = min_date, max_date

df = df_full[
    (df_full["collection_date"] >= d_start)
    & (df_full["collection_date"] <= d_end)
    & (df_full["city"].isin(sel_cities))
    & (df_full["lab_name"].isin(sel_labs))
    & (df_full["courier_name"].isin(sel_couriers))
    & (df_full["test_name"].isin(sel_tests))
    & (df_full["sample_status"].isin(sel_statuses))
].copy()

# ═══════════════════════════════════════════════════════════════════════════
# Header
# ═══════════════════════════════════════════════════════════════════════════
st.markdown(
    """
    <div style="background:linear-gradient(90deg,#0f172a,#1e3a5f);
                border-radius:14px;padding:24px 32px;margin-bottom:24px;">
        <h1 style="color:#38bdf8;margin:0;font-size:1.8rem;font-weight:700;letter-spacing:-0.02em;">
            🏥 Diagnostic Lab Operational Analytics
        </h1>
        <p style="color:#94a3b8;margin:6px 0 0 0;font-size:0.92rem;">
            Sample Logistics · Courier Performance · Lab Efficiency · TAT Analysis
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ═══════════════════════════════════════════════════════════════════════════
# Chart helpers
# ═══════════════════════════════════════════════════════════════════════════
BRAND_BLUE = "#38bdf8"
CHART_COLORS = ["#38bdf8", "#818cf8", "#34d399", "#fb923c", "#f472b6"]
CHART_BG = "rgba(0,0,0,0)"
AXIS_COLOR = "#475569"
GRID_COLOR = "#1e293b"

def apply_chart_style(fig: go.Figure, height: int = 340) -> go.Figure:
    fig.update_layout(
        height=height,
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_BG,
        font=dict(family="Inter", color="#e2e8f0", size=12),
        margin=dict(l=12, r=12, t=36, b=12),
        legend=dict(bgcolor="rgba(0,0,0,0)", font_size=11),
        xaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR, color=AXIS_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR, color=AXIS_COLOR),
    )
    return fig


def kpi(label: str, value, sub: str = "") -> str:
    return (
        f'<div class="kpi-card">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="kpi-sub">{sub}</div>'
        f"</div>"
    )


# ═══════════════════════════════════════════════════════════════════════════
# Tabs
# ═══════════════════════════════════════════════════════════════════════════
tab_overview, tab_lab, tab_courier, tab_test, tab_journey = st.tabs([
    "📊 Executive Overview",
    "🏥 Lab Performance",
    "🚚 Courier Performance",
    "🔬 Test Type Analytics",
    "🗺 Sample Journey",
])


# ┌───────────────────────────────────────────────────────────────────────┐
# │ A. EXECUTIVE OVERVIEW                                                 │
# └───────────────────────────────────────────────────────────────────────┘
with tab_overview:
    if df.empty:
        st.warning("No data matches the current filters. Adjust the sidebar filters.")
        st.stop()

    # ── KPI Cards ──────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Key Performance Indicators</div>', unsafe_allow_html=True)

    total   = m.total_samples(df)
    done    = m.completed_samples(df)
    rej     = m.rejected_samples(df)
    delayed = m.delayed_samples(df)
    sla_br  = m.sla_breach_rate(df)
    avg_tat = m.avg_tat_hours(df)
    avg_cou = m.avg_courier_transit_hours(df)
    avg_lab = m.avg_lab_processing_hours(df)

    _rej_rate_pct = round(rej / total * 100, 1) if total else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(kpi("Total Samples", f"{total:,}", "All time in selection"), unsafe_allow_html=True)
    with c2: st.markdown(kpi("Completed", f"{done:,}", f"{done/total*100:.1f}% of total" if total else "—"), unsafe_allow_html=True)
    with c3: st.markdown(kpi("Rejected", f"{rej:,}", f"{_rej_rate_pct}% rejection rate"), unsafe_allow_html=True)
    with c4: st.markdown(kpi("SLA Breach Rate", f"{sla_br}%", "Excl. rejected samples"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c5, c6, c7, c8 = st.columns(4)
    with c5: st.markdown(kpi("Avg Total TAT", f"{avg_tat} hrs", "Collection → Report release"), unsafe_allow_html=True)
    with c6: st.markdown(kpi("Avg Courier Transit", f"{avg_cou} hrs", "Pickup → Lab delivery"), unsafe_allow_html=True)
    with c7: st.markdown(kpi("Avg Lab Processing", f"{avg_lab} hrs", "Receipt → Test completion"), unsafe_allow_html=True)
    with c8: st.markdown(kpi("Delayed Samples", f"{delayed:,}", f"{delayed/total*100:.1f}% of total" if total else "—"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts row ─────────────────────────────────────────────────────
    col_donut, col_trend = st.columns([1, 2])

    with col_donut:
        st.markdown('<div class="section-title">Sample Status Split</div>', unsafe_allow_html=True)
        status_counts = df["sample_status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        fig_donut = px.pie(
            status_counts, names="Status", values="Count",
            hole=0.55, color_discrete_sequence=CHART_COLORS,
        )
        fig_donut.update_traces(textinfo="percent+label", pull=[0.03] * len(status_counts))
        fig_donut = apply_chart_style(fig_donut, height=320)
        fig_donut.update_layout(showlegend=False)
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_trend:
        st.markdown('<div class="section-title">Daily Sample Volume Trend</div>', unsafe_allow_html=True)
        daily = m.daily_volume(df)
        fig_trend = px.line(
            daily, x="collection_date", y="count", color="sample_status",
            markers=True, color_discrete_sequence=CHART_COLORS,
            labels={"collection_date": "Date", "count": "Sample Count", "sample_status": "Status"},
        )
        fig_trend = apply_chart_style(fig_trend, height=320)
        st.plotly_chart(fig_trend, use_container_width=True)

    # ── Priority split ─────────────────────────────────────────────────
    st.markdown('<div class="section-title">Sample Priority Distribution</div>', unsafe_allow_html=True)
    priority_df = df["priority_flag"].value_counts().reset_index()
    priority_df.columns = ["Priority", "Count"]
    fig_priority = px.bar(
        priority_df, x="Priority", y="Count",
        color="Priority", color_discrete_sequence=CHART_COLORS,
        labels={"Count": "Number of Samples"},
        text="Count",
    )
    fig_priority.update_traces(textposition="outside")
    fig_priority = apply_chart_style(fig_priority, height=280)
    fig_priority.update_layout(showlegend=False)
    st.plotly_chart(fig_priority, use_container_width=True)


# ┌───────────────────────────────────────────────────────────────────────┐
# │ B. LAB PERFORMANCE                                                    │
# └───────────────────────────────────────────────────────────────────────┘
with tab_lab:
    if df.empty:
        st.warning("No data matches the current filters.")
    else:
        lab_df = m.lab_summary(df)

        st.markdown('<div class="section-title">Samples Handled by Lab</div>', unsafe_allow_html=True)
        fig_lab_vol = px.bar(
            lab_df, x="lab_name", y="sample_count",
            color="sample_count", color_continuous_scale="Blues",
            labels={"lab_name": "Lab", "sample_count": "Sample Count"},
            text="sample_count",
        )
        fig_lab_vol.update_traces(textposition="outside")
        fig_lab_vol = apply_chart_style(fig_lab_vol)
        fig_lab_vol.update_coloraxes(showscale=False)
        st.plotly_chart(fig_lab_vol, use_container_width=True)

        col_tat, col_rej = st.columns(2)

        with col_tat:
            st.markdown('<div class="section-title">Avg TAT by Lab (hrs)</div>', unsafe_allow_html=True)
            fig_tat = px.bar(
                lab_df.dropna(subset=["avg_tat_hours"]),
                x="avg_tat_hours", y="lab_name", orientation="h",
                color="avg_tat_hours", color_continuous_scale="Blues",
                labels={"avg_tat_hours": "Avg TAT (hrs)", "lab_name": "Lab"},
                text="avg_tat_hours",
            )
            fig_tat.update_traces(texttemplate="%{text:.1f}h", textposition="outside")
            fig_tat = apply_chart_style(fig_tat)
            fig_tat.update_coloraxes(showscale=False)
            st.plotly_chart(fig_tat, use_container_width=True)

        with col_rej:
            st.markdown('<div class="section-title">Rejection Rate by Lab (%)</div>', unsafe_allow_html=True)
            fig_rej = px.bar(
                lab_df,
                x="rejection_rate_pct", y="lab_name", orientation="h",
                color="rejection_rate_pct", color_continuous_scale="Reds",
                labels={"rejection_rate_pct": "Rejection Rate (%)", "lab_name": "Lab"},
                text="rejection_rate_pct",
            )
            fig_rej.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig_rej = apply_chart_style(fig_rej)
            fig_rej.update_coloraxes(showscale=False)
            st.plotly_chart(fig_rej, use_container_width=True)

        st.markdown('<div class="section-title">SLA Breach Rate by Lab (%)</div>', unsafe_allow_html=True)
        fig_sla = px.bar(
            lab_df,
            x="lab_name", y="sla_breach_rate_pct",
            color="sla_breach_rate_pct", color_continuous_scale="Oranges",
            labels={"lab_name": "Lab", "sla_breach_rate_pct": "SLA Breach Rate (%)"},
            text="sla_breach_rate_pct",
        )
        fig_sla.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_sla = apply_chart_style(fig_sla)
        fig_sla.update_coloraxes(showscale=False)
        st.plotly_chart(fig_sla, use_container_width=True)

        # Overloaded labs table
        st.markdown('<div class="section-title">Lab Load Summary</div>', unsafe_allow_html=True)
        cap_df = df.groupby("lab_name", as_index=False).agg(
            total_samples=("sample_id", "count"),
            capacity_per_day=("capacity_per_day", "first"),
        )
        days = max(1, (d_end - d_start).days + 1) if hasattr(d_start, "__sub__") else 21
        cap_df["avg_daily_samples"] = (cap_df["total_samples"] / days).round(1)
        cap_df["load_pct"] = (cap_df["avg_daily_samples"] / cap_df["capacity_per_day"] * 100).round(1)
        cap_df["status"] = cap_df["load_pct"].apply(
            lambda x: "🔴 Overloaded" if x > 80 else ("🟡 Near Capacity" if x > 60 else "🟢 Normal")
        )
        st.dataframe(
            cap_df[["lab_name", "total_samples", "capacity_per_day", "avg_daily_samples", "load_pct", "status"]]
            .rename(columns={
                "lab_name": "Lab", "total_samples": "Total Samples",
                "capacity_per_day": "Daily Capacity", "avg_daily_samples": "Avg Daily Samples",
                "load_pct": "Load %", "status": "Status",
            }),
            use_container_width=True, hide_index=True,
        )


# ┌───────────────────────────────────────────────────────────────────────┐
# │ C. COURIER PERFORMANCE                                                │
# └───────────────────────────────────────────────────────────────────────┘
with tab_courier:
    if df.empty:
        st.warning("No data matches the current filters.")
    else:
        cou_df = m.courier_summary(df)

        st.markdown('<div class="section-title">Samples Transported by Courier</div>', unsafe_allow_html=True)
        fig_cou_vol = px.bar(
            cou_df, x="courier_name", y="sample_count",
            color="sample_count", color_continuous_scale="Blues",
            labels={"courier_name": "Courier", "sample_count": "Samples"},
            text="sample_count",
        )
        fig_cou_vol.update_traces(textposition="outside")
        fig_cou_vol = apply_chart_style(fig_cou_vol)
        fig_cou_vol.update_coloraxes(showscale=False)
        st.plotly_chart(fig_cou_vol, use_container_width=True)

        col_transit, col_delay = st.columns(2)

        with col_transit:
            st.markdown('<div class="section-title">Avg Transit Time by Courier (hrs)</div>', unsafe_allow_html=True)
            fig_transit = px.bar(
                cou_df.dropna(subset=["avg_transit_hours"]),
                x="avg_transit_hours", y="courier_name", orientation="h",
                color="avg_transit_hours", color_continuous_scale="Blues",
                labels={"avg_transit_hours": "Avg Transit (hrs)", "courier_name": "Courier"},
                text="avg_transit_hours",
            )
            fig_transit.update_traces(texttemplate="%{text:.2f}h", textposition="outside")
            fig_transit = apply_chart_style(fig_transit)
            fig_transit.update_coloraxes(showscale=False)
            st.plotly_chart(fig_transit, use_container_width=True)

        with col_delay:
            st.markdown('<div class="section-title">Delay Rate by Courier (%)</div>', unsafe_allow_html=True)
            fig_delay = px.bar(
                cou_df,
                x="delay_rate_pct", y="courier_name", orientation="h",
                color="delay_rate_pct", color_continuous_scale="Reds",
                labels={"delay_rate_pct": "Delay Rate (%)", "courier_name": "Courier"},
                text="delay_rate_pct",
            )
            fig_delay.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig_delay = apply_chart_style(fig_delay)
            fig_delay.update_coloraxes(showscale=False)
            st.plotly_chart(fig_delay, use_container_width=True)

        st.markdown('<div class="section-title">SLA Compliance by Courier (%)</div>', unsafe_allow_html=True)
        fig_on_time = px.bar(
            cou_df,
            x="courier_name", y="on_time_rate_pct",
            color="on_time_rate_pct", color_continuous_scale="Greens",
            labels={"courier_name": "Courier", "on_time_rate_pct": "On-Time Rate (%)"},
            text="on_time_rate_pct",
        )
        fig_on_time.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_on_time = apply_chart_style(fig_on_time)
        fig_on_time.update_coloraxes(showscale=False)
        st.plotly_chart(fig_on_time, use_container_width=True)

        # Courier summary table
        st.markdown('<div class="section-title">Courier Summary Table</div>', unsafe_allow_html=True)
        st.dataframe(
            cou_df.rename(columns={
                "courier_name": "Courier", "sample_count": "Samples",
                "avg_transit_hours": "Avg Transit (hrs)",
                "delay_rate_pct": "Delay Rate (%)", "on_time_rate_pct": "On-Time Rate (%)",
            }),
            use_container_width=True, hide_index=True,
        )


# ┌───────────────────────────────────────────────────────────────────────┐
# │ D. TEST TYPE ANALYTICS                                                │
# └───────────────────────────────────────────────────────────────────────┘
with tab_test:
    if df.empty:
        st.warning("No data matches the current filters.")
    else:
        test_df = m.test_type_summary(df)

        st.markdown('<div class="section-title">Volume by Test Type</div>', unsafe_allow_html=True)
        fig_tvol = px.bar(
            test_df, x="test_name", y="sample_count",
            color="is_critical_test",
            color_discrete_map={True: "#f472b6", False: "#38bdf8"},
            labels={"test_name": "Test", "sample_count": "Samples",
                    "is_critical_test": "Critical?"},
            text="sample_count",
        )
        fig_tvol.update_traces(textposition="outside")
        fig_tvol = apply_chart_style(fig_tvol)
        st.plotly_chart(fig_tvol, use_container_width=True)

        col_tat2, col_rej2 = st.columns(2)

        with col_tat2:
            st.markdown('<div class="section-title">Avg TAT by Test Type (hrs)</div>', unsafe_allow_html=True)
            fig_ttat = px.bar(
                test_df.dropna(subset=["avg_tat_hours"]).sort_values("avg_tat_hours", ascending=False),
                x="avg_tat_hours", y="test_name", orientation="h",
                color="avg_tat_hours", color_continuous_scale="Blues",
                labels={"avg_tat_hours": "Avg TAT (hrs)", "test_name": "Test"},
                text="avg_tat_hours",
            )
            fig_ttat.update_traces(texttemplate="%{text:.1f}h", textposition="outside")
            fig_ttat = apply_chart_style(fig_ttat, height=380)
            fig_ttat.update_coloraxes(showscale=False)
            st.plotly_chart(fig_ttat, use_container_width=True)

        with col_rej2:
            st.markdown('<div class="section-title">Rejection Rate by Test Type (%)</div>', unsafe_allow_html=True)
            fig_trej = px.bar(
                test_df.sort_values("rejection_rate_pct", ascending=False),
                x="rejection_rate_pct", y="test_name", orientation="h",
                color="rejection_rate_pct", color_continuous_scale="Reds",
                labels={"rejection_rate_pct": "Rejection Rate (%)", "test_name": "Test"},
                text="rejection_rate_pct",
            )
            fig_trej.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig_trej = apply_chart_style(fig_trej, height=380)
            fig_trej.update_coloraxes(showscale=False)
            st.plotly_chart(fig_trej, use_container_width=True)

        # Critical vs Normal summary
        st.markdown('<div class="section-title">Critical vs Normal Tests</div>', unsafe_allow_html=True)
        crit_df = test_df.copy()
        crit_df["type"] = crit_df["is_critical_test"].map({True: "Critical", False: "Normal"})
        crit_sum = crit_df.groupby("type", as_index=False)["sample_count"].sum()
        fig_crit = px.bar(
            crit_sum, x="type", y="sample_count",
            color="type", color_discrete_map={"Critical": "#f472b6", "Normal": "#38bdf8"},
            labels={"type": "Test Category", "sample_count": "Sample Count"},
            text="sample_count",
        )
        fig_crit.update_traces(textposition="outside")
        fig_crit = apply_chart_style(fig_crit, height=280)
        fig_crit.update_layout(showlegend=False)
        st.plotly_chart(fig_crit, use_container_width=True)


# ┌───────────────────────────────────────────────────────────────────────┐
# │ E. SAMPLE JOURNEY DETAIL                                              │
# └───────────────────────────────────────────────────────────────────────┘
with tab_journey:
    st.markdown('<div class="section-title">Full Sample Journey — Filterable Detail Table</div>', unsafe_allow_html=True)
    st.caption(
        "Each row represents one sample's complete lifecycle: "
        "collection → pickup → delivery → lab receipt → testing → report release."
    )

    # Extra filter: sample ID search
    search_id = st.text_input("🔍 Search by Sample ID (e.g. SMP000042)", value="")

    # Build display table
    journey_cols = [
        "sample_id", "test_name", "city", "lab_name", "courier_name",
        "sample_status", "priority_flag",
        "sample_collected_at", "pickup_time", "delivery_time",
        "lab_received_at", "test_started_at", "test_completed_at", "report_released_at",
        "courier_transit_hours", "lab_processing_hours", "total_tat_hours",
        "promised_tat_hours", "sla_breach", "rejection_reason",
    ]
    available_cols = [c for c in journey_cols if c in df.columns]
    jdf = df[available_cols].copy()

    if search_id.strip():
        jdf = jdf[jdf["sample_id"].str.contains(search_id.strip(), case=False, na=False)]

    # Round numeric columns
    for col in ["courier_transit_hours", "lab_processing_hours", "total_tat_hours"]:
        if col in jdf.columns:
            jdf[col] = jdf[col].round(2)

    # Rename for display
    rename_map = {
        "sample_id": "Sample ID", "test_name": "Test", "city": "City",
        "lab_name": "Lab", "courier_name": "Courier",
        "sample_status": "Status", "priority_flag": "Priority",
        "sample_collected_at": "Collected At", "pickup_time": "Pickup Time",
        "delivery_time": "Delivery Time", "lab_received_at": "Lab Received At",
        "test_started_at": "Test Started", "test_completed_at": "Test Completed",
        "report_released_at": "Report Released",
        "courier_transit_hours": "Transit (hrs)", "lab_processing_hours": "Lab Processing (hrs)",
        "total_tat_hours": "Total TAT (hrs)", "promised_tat_hours": "Promised TAT (hrs)",
        "sla_breach": "SLA Breach", "rejection_reason": "Rejection Reason",
    }
    jdf = jdf.rename(columns={k: v for k, v in rename_map.items() if k in jdf.columns})

    st.dataframe(jdf, use_container_width=True, hide_index=True, height=480)

    st.caption(
        f"Showing **{len(jdf):,}** records. "
        "Use the sidebar filters or the search box above to narrow down."
    )

# ═══════════════════════════════════════════════════════════════════════════
# Footer
# ═══════════════════════════════════════════════════════════════════════════
st.markdown(
    """
    <div style="text-align:center;color:#475569;font-size:0.78rem;margin-top:40px;padding-top:16px;
                border-top:1px solid #1e293b;">
        Diagnostic Lab Operational Analytics · Powered by Streamlit &amp; Plotly ·
        Data: Synthetic (Demo) · <strong>No cloud dependencies</strong>
    </div>
    """,
    unsafe_allow_html=True,
)
