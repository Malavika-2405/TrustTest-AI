import streamlit as st
import pandas as pd
import uuid

from database.db import (
    insert_conversation_turn,
    get_conversation_history,
    get_all_conversation_sessions
)


def analyze_consistency(previous_responses, current_response):
    previous_text = " ".join(previous_responses).lower()
    current_text = current_response.lower()

    contradiction_pairs = [
        ("yes", "no"),
        ("true", "false"),
        ("always", "never"),
        ("increase", "decrease"),
        ("safe", "unsafe")
    ]

    for first, second in contradiction_pairs:
        if first in previous_text and second in current_text:
            return 40.0, True, "Possible contradiction detected."

        if second in previous_text and first in current_text:
            return 40.0, True, "Possible contradiction detected."

    return 100.0, False, "No simple contradiction pattern detected."


def render_conversation_testing():
    st.title("Multi-Turn Conversation Testing")
    st.caption("Record conversations and inspect possible contradictions.")

    sessions = get_all_conversation_sessions()

    # Session IDs are strings, not dictionaries.
    session_options = {
        f"Session: {session_id}": session_id
        for session_id in sessions
    }

    choice = st.radio(
        "Choose conversation session",
        ["Create New Session", "Continue Existing Session"]
    )

    if choice == "Create New Session":
        session_id = str(uuid.uuid4())
        st.info(f"New session ID: {session_id}")
    else:
        if not session_options:
            st.warning("No existing sessions found. Create a new session first.")
            return

        selected = st.selectbox(
            "Select Session",
            list(session_options.keys())
        )

        session_id = session_options[selected]

    history = get_conversation_history(session_id)

    previous_responses = [
        turn["content"]
        for turn in history
        if turn["role"] == "assistant"
    ]

    st.subheader("Conversation History")

    if history:
        st.dataframe(
            pd.DataFrame(history),
            use_container_width=True
        )
    else:
        st.info("No conversation turns recorded yet.")

    st.subheader("Add Conversation Turn")

    with st.form("conversation_form"):
        user_message = st.text_area("User Message")
        assistant_response = st.text_area("AI Assistant Response")

        submitted = st.form_submit_button("Analyze and Save Turn")

    if submitted:
        if not user_message.strip() or not assistant_response.strip():
            st.warning("Enter both the user message and AI response.")
        else:
            score, contradiction, notes = analyze_consistency(
                previous_responses,
                assistant_response
            )

            next_index = max(
                [turn["turn_index"] for turn in history],
                default=0
            ) + 1

            insert_conversation_turn(
                session_id,
                next_index,
                "user",
                user_message.strip(),
                100.0,
                False,
                False,
                "User message recorded."
            )

            insert_conversation_turn(
                session_id,
                next_index + 1,
                "assistant",
                assistant_response.strip(),
                score,
                contradiction,
                False,
                notes
            )

            if contradiction:
                st.warning(notes)
            else:
                st.success(notes)

            st.success("Conversation turn saved successfully!")
            st.rerun()

