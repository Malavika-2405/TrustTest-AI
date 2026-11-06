
import streamlit as st
import pandas as pd

from database.db import (
    get_all_datasets,
    get_all_test_cases,
    create_evaluation_run,
    insert_evaluation_result,
    update_evaluation_run_summary
)

from modules.semantic_evaluator import calculate_semantic_similarity


def evaluate_response(expected, actual):
    score = calculate_semantic_similarity(expected, actual)

    return {
        "semantic_similarity": score,
        "overall_score": score
    }


def render_evaluation_engine():
    st.title("AI Evaluation Engine")
    st.caption("Evaluate AI responses using local semantic similarity.")

    st.info(
        "This evaluation uses a Sentence Transformers model to compare "
        "the meaning of reference answers and AI responses. "
        "Semantic similarity does not independently verify factual correctness."
    )

    datasets = get_all_datasets()

    if not datasets:
        st.warning("Create a dataset first.")
        return

    options = {
        f"{d['name']} (ID: {d['id']})": d['id']
        for d in datasets
    }

    selected = st.selectbox("Select Dataset", list(options.keys()))
    dataset_id = options[selected]

    cases = get_all_test_cases(dataset_id)

    if not cases:
        st.info("No test cases found. Add test cases first.")
        return

    st.subheader("Enter AI Responses")

    responses = {}

    for index, case in enumerate(cases):
        st.markdown(
            f"**Test Case {index + 1}: {case['question']}**"
        )

        responses[case["id"]] = st.text_area(
            "AI Generated Response",
            key=f"eval_response_{case['id']}"
        )

    if st.button("Run Evaluation", type="primary"):

        if any(not value.strip() for value in responses.values()):
            st.warning("Enter an AI response for every test case.")
            return

        results = []

        try:
            with st.spinner("Evaluating responses using the semantic model..."):

                for case in cases:
                    actual = responses[case["id"]]

                    metrics = evaluate_response(
                        case["expected_answer"],
                        actual
                    )

                    results.append({
                        "case": case,
                        "actual": actual,
                        "score": metrics["semantic_similarity"],
                        "question": case["question"]
                    })

        except Exception as error:
            st.error(f"Evaluation failed: {error}")
            return

        try:
            run_id = create_evaluation_run(
                "Semantic Similarity Evaluation",
                "Sentence Transformers",
                "all-MiniLM-L6-v2"
            )

            display_results = []

            for result in results:
                score = result["score"]
                passed = score >= 70

                insert_evaluation_result(
                    run_id,
                    result["case"]["id"],
                    result["question"],
                    result["actual"],
                    result["case"]["expected_answer"],
                    result["case"].get("context") or "",
                    "semantic_similarity",
                    score,
                    passed,
                    f"Semantic similarity score: {score}%"
                )

                display_results.append({
                    "Question": result["question"],
                    "Semantic Similarity": score,
                    "Status": "PASS" if passed else "REVIEW"
                })

            average_score = sum(
                result["score"] for result in results
            ) / len(results)

            update_evaluation_run_summary(
                run_id,
                len(results),
                average_score,
                "COMPLETED"
            )

        except Exception as error:
            st.error(f"Unable to save evaluation results: {error}")
            return

        # Evaluation Summary

        st.success("Semantic evaluation completed successfully!")

        passed_count = sum(
            1 for result in display_results
            if result["Status"] == "PASS"
        )

        review_count = len(display_results) - passed_count

        st.subheader("Evaluation Summary")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Average Similarity",
                f"{average_score:.2f}%"
            )

        with col2:
            st.metric(
                "Passed Test Cases",
                passed_count
            )

        with col3:
            st.metric(
                "Needs Review",
                review_count
            )

        # Individual Test Results

        st.subheader("Individual Test Results")

        st.dataframe(
            pd.DataFrame(display_results),
            use_container_width=True,
            hide_index=True
        )


