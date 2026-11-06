
import streamlit as st
import pandas as pd

from database.db import (
    create_dataset,
    get_all_datasets,
    insert_test_case,
    get_all_test_cases
)


def render_dataset_manager():
    st.title("Golden Dataset Manager")
    st.caption("Manage trusted datasets and expected AI responses.")

    tab1, tab2 = st.tabs(["Datasets", "Test Cases"])

    with tab1:
        st.subheader("Create Dataset")

        with st.form("create_dataset_form"):
            name = st.text_input("Dataset Name")
            description = st.text_area("Description")

            submitted = st.form_submit_button("Create Dataset")

            if submitted:
                if name.strip():
                    try:
                        create_dataset(name.strip(), description.strip())
                        st.success("Dataset created successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("Enter a dataset name.")

        datasets = get_all_datasets()

        if datasets:
            st.subheader("Available Datasets")
            st.dataframe(pd.DataFrame(datasets), use_container_width=True)
        else:
            st.info("No datasets created yet.")

    with tab2:
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

        with st.form("add_test_case_form"):
            category = st.selectbox(
                "Category",
                ["General", "Accuracy", "Reasoning", "Safety", "Other"]
            )
            question = st.text_area("User Question")
            expected_answer = st.text_area("Expected Answer")
            context = st.text_area("Reference Context (Optional)")

            submitted = st.form_submit_button("Add Test Case")

            if submitted:
                if question.strip() and expected_answer.strip():
                    try:
                        insert_test_case(
                            dataset_id,
                            category,
                            question.strip(),
                            expected_answer.strip(),
                            context.strip()
                        )
                        st.success("Test case added successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("Question and expected answer are required.")

        st.subheader("Existing Test Cases")

        cases = get_all_test_cases(dataset_id)

        if cases:
            st.dataframe(pd.DataFrame(cases), use_container_width=True)
        else:
            st.info("No test cases available in this dataset.")
