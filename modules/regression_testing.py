
import streamlit as st
import pandas as pd

from database.db import (
    get_evaluation_runs,
    insert_regression_run,
    get_regression_runs
)


def render_regression_testing():
    st.title("Regression Testing")
    st.caption("Compare evaluation runs to identify quality changes.")

    runs = get_evaluation_runs()

    if len(runs) < 2:
        st.info(
            "You need at least two completed evaluation runs "
            "before you can compare results."
        )
    else:
        options = {
            f"Run #{run['id']} - {run['run_name']} "
            f"({run['overall_score']}%)": run['id']
            for run in runs
        }

        run_labels = list(options.keys())

        st.subheader("Compare Evaluation Runs")

        baseline_label = st.selectbox(
            "Baseline Run (Previous)",
            run_labels,
            key="baseline_run"
        )

        candidate_labels = [
            label for label in run_labels
            if options[label] != options[baseline_label]
        ]

        candidate_label = st.selectbox(
            "Candidate Run (New)",
            candidate_labels,
            key="candidate_run"
        )

        threshold = st.number_input(
            "Allowed Score Drop (%)",
            min_value=0.0,
            max_value=100.0,
            value=5.0,
            step=1.0
        )

        if st.button("Run Regression Test", type="primary"):
            baseline_id = options[baseline_label]
            candidate_id = options[candidate_label]

            baseline = next(
                run for run in runs if run["id"] == baseline_id
            )

            candidate = next(
                run for run in runs if run["id"] == candidate_id
            )

            baseline_score = float(baseline["overall_score"])
            candidate_score = float(candidate["overall_score"])

            score_delta = round(
                candidate_score - baseline_score, 2
            )

            status = (
                "PASSED" if score_delta >= -threshold else "FAILED"
            )

            output = (
                f"Baseline score: {baseline_score}%\n"
                f"Candidate score: {candidate_score}%\n"
                f"Score change: {score_delta}%\n"
                f"Allowed drop: {threshold}%\n"
                f"Regression status: {status}"
            )

            insert_regression_run(
                "Evaluation Run Comparison",
                baseline_id,
                candidate_id,
                baseline_score,
                candidate_score,
                score_delta,
                threshold,
                status,
                output
            )

            if status == "PASSED":
                st.success("Regression test passed!")
            else:
                st.error("Regression detected!")

            st.metric(
                "Score Change",
                f"{score_delta:+.2f}%",
                delta=f"{score_delta:+.2f}%"
            )

    st.divider()
    st.subheader("Regression Test History")

    history = get_regression_runs()

    if history:
        st.dataframe(
            pd.DataFrame(history),
            use_container_width=True
        )
    else:
        st.info("No regression tests performed yet.")
