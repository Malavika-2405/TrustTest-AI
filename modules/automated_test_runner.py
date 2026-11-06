
import subprocess
import sys
from pathlib import Path

import streamlit as st


def render_automated_test_runner():
    st.title("Automated Test Runner")
    st.caption("Execute and monitor automated tests using Pytest.")

    project_root = Path(__file__).resolve().parent.parent
    tests_folder = project_root / "tests"

    st.subheader("Test Suite")

    if not tests_folder.exists():
        st.warning("The tests folder was not found.")
        return

    test_files = sorted(tests_folder.glob("test_*.py"))

    if not test_files:
        st.info("No automated test files were found.")
        return

    st.write("Available test files:")

    for test_file in test_files:
        st.write(f"• {test_file.name}")

    if st.button("Run All Automated Tests", type="primary"):
        command = [
            sys.executable,
            "-m",
            "pytest",
            str(tests_folder),
            "-v",
            "--tb=short"
        ]

        with st.spinner("Running automated tests..."):
            try:
                result = subprocess.run(
                    command,
                    cwd=str(project_root),
                    capture_output=True,
                    text=True,
                    timeout=300
                )

                output = result.stdout + "\n" + result.stderr

                st.subheader("Test Execution Results")

                if result.returncode == 0:
                    st.success("All automated tests passed!")
                else:
                    st.error("Some tests failed or pytest encountered an error.")

                st.code(output or "No test output available.", language="text")

                st.metric("Pytest Exit Code", result.returncode)

            except subprocess.TimeoutExpired:
                st.error("Test execution timed out after 5 minutes.")

            except Exception as error:
                st.error(f"Unable to execute tests: {error}")
