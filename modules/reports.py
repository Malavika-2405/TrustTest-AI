
import streamlit as st
import pandas as pd

from database.db import (
    get_evaluation_runs,
    get_evaluation_results
)


def render_reports():
    st.title("Evaluation Reports")
    st.caption("View, compare and download AI evaluation reports.")

    runs = get_evaluation_runs()

    if not runs:
        st.info("No evaluation runs available. Run an evaluation first.")
        return

    # Evaluation Run Selection
    run_options = {
        f"Run #{run['id']} - {run['run_name']}": run["id"]
        for run in runs
    }

    selected_label = st.selectbox(
        "Select Evaluation Run",
        list(run_options.keys())
    )

    run_id = run_options[selected_label]

    results = get_evaluation_results(run_id)

    if not results:
        st.info("No results found for this evaluation run.")
        return

    df = pd.DataFrame(results)

    # Evaluation Summary
    st.subheader("Evaluation Summary")

    if "metric_score" not in df.columns:
        st.warning("Metric scores are unavailable for this run.")
        return

    df["metric_score"] = pd.to_numeric(
        df["metric_score"], errors="coerce"
    )

    df = df.dropna(subset=["metric_score"])

    if df.empty:
        st.info("No valid evaluation scores are available.")
        return

    average_score = df["metric_score"].mean()

    passed_count = (
        df["passed"].fillna(0).astype(bool).sum()
        if "passed" in df.columns else 0
    )

    total_count = len(df)
    review_count = total_count - passed_count

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Test Cases", total_count)

    with col2:
        st.metric("Average Similarity", f"{average_score:.2f}%")

    with col3:
        st.metric("Passed", int(passed_count))

    with col4:
        st.metric("Needs Review", int(review_count))

    # Metric Summary
    st.subheader("Metric-wise Performance")

    if "metric_name" in df.columns:
        summary = (
            df.groupby("metric_name")["metric_score"]
            .mean()
            .reset_index()
        )

        summary.columns = ["Metric", "Average Score (%)"]

        st.dataframe(
            summary,
            use_container_width=True,
            hide_index=True
        )

    # Individual Test Scores
    st.subheader("Individual Test Scores")

    chart_df = df.copy()

    if "question" in chart_df.columns:
        chart_df["Test Case"] = [
            f"Test {i + 1}" for i in range(len(chart_df))
        ]
        st.bar_chart(
            chart_df.set_index("Test Case")["metric_score"]
        )

    # Detailed Results
    st.subheader("Detailed Evaluation Results")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # Evaluation History
    st.subheader("Evaluation History")

    history = []

    for run in runs:
        run_results = get_evaluation_results(run["id"])

        if run_results:
            scores = [
                float(item["metric_score"])
                for item in run_results
                if item.get("metric_score") is not None
            ]

            if scores:
                history.append({
                    "Run": f"Run #{run['id']}",
                    "Average Score": sum(scores) / len(scores)
                })

    if history:
        history_df = pd.DataFrame(history)

        st.line_chart(
            history_df.set_index("Run")["Average Score"]
        )

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )

    # CSV Download
    st.subheader("Download Report")

    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Evaluation Report (CSV)",
        data=csv_data,
        file_name=f"evaluation_report_run_{run_id}.csv",
        mime="text/csv"
    )
