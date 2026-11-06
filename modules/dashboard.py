
import streamlit as st
import pandas as pd
import plotly.express as px

from database.db import get_db_connection


def render_dashboard():
    st.title("TrustTest AI Dashboard")
    st.caption("Monitor AI quality, reliability and evaluation performance.")

    # Fetch evaluation history
    with get_db_connection() as conn:
        runs = pd.read_sql_query(
            "SELECT * FROM evaluation_runs ORDER BY id DESC",
            conn
        )

    if runs.empty:
        st.info(
            "No evaluation runs available yet. "
            "Run an evaluation to see your dashboard."
        )
        return

    # Prepare score data
    if "overall_score" in runs.columns:
        runs["overall_score"] = pd.to_numeric(
            runs["overall_score"],
            errors="coerce"
        )
    else:
        runs["overall_score"] = pd.NA

    valid_scores = runs["overall_score"].dropna()

    average_score = (
        valid_scores.mean()
        if not valid_scores.empty else None
    )

    latest_run = runs.iloc[0]

    latest_score = latest_run["overall_score"]

    latest_status = str(
        latest_run.get("status", "Unknown")
    )

    # Dashboard Metrics
    st.subheader("Performance Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Evaluation Runs",
            len(runs)
        )

    with col2:
        st.metric(
            "Average Score",
            f"{average_score:.2f}%" if average_score is not None else "N/A"
        )

    with col3:
        st.metric(
            "Latest Score",
            f"{latest_score:.2f}%" if pd.notna(latest_score) else "N/A"
        )

    with col4:
        st.metric(
            "Latest Run Status",
            latest_status
        )

    # Evaluation Trend
    chart_data = runs.dropna(
        subset=["overall_score"]
    ).sort_values("id")

    if not chart_data.empty:
        st.subheader("Evaluation Score Trend")

        fig = px.line(
            chart_data,
            x="id",
            y="overall_score",
            markers=True,
            title="AI Evaluation Performance",
            labels={
                "id": "Evaluation Run",
                "overall_score": "Average Score (%)"
            },
            hover_data=["status"] if "status" in chart_data.columns else None
        )

        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Evaluation Run",
            yaxis_title="Average Score (%)",
            yaxis=dict(range=[0, 100]),
            hovermode="x unified"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # Recent Evaluation History
    st.subheader("Recent Evaluation Runs")

    display_columns = [
        column for column in [
            "id",
            "run_name",
            "engine",
            "model_name",
            "total_samples",
            "overall_score",
            "status",
            "created_at"
        ]
        if column in runs.columns
    ]

    recent_runs = runs[display_columns].head(10).copy()

    st.dataframe(
        recent_runs,
        use_container_width=True,
        hide_index=True
    )
