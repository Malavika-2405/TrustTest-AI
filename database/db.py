import os
import sqlite3
from contextlib import contextmanager
from typing import Any, Dict, List, Optional

DB_FILE = os.getenv("DB_PATH", "trusttest.db")
SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "schema.sql")


@contextmanager
def get_db_connection():
    db_dir = os.path.dirname(os.path.abspath(DB_FILE))
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    with get_db_connection() as conn:
        with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
            conn.executescript(f.read())


def execute_query(query: str, params: tuple = ()) -> List[sqlite3.Row]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()


def execute_commit(query: str, params: tuple = ()) -> int:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.lastrowid if cursor.lastrowid is not None else 0


def create_dataset(name: str, description: str = "") -> int:
    return execute_commit(
        "INSERT INTO datasets (name, description) VALUES (?, ?)",
        (name, description),
    )


def get_all_datasets() -> List[Dict[str, Any]]:
    rows = execute_query("SELECT * FROM datasets ORDER BY created_at DESC")
    return [dict(r) for r in rows]


def delete_dataset(dataset_id: int):
    execute_commit("DELETE FROM datasets WHERE id = ?", (dataset_id,))


def insert_test_case(
    dataset_id: Optional[int],
    category: str,
    question: str,
    expected_answer: str,
    context: str = "",
) -> int:
    query = """
    INSERT INTO test_cases (dataset_id, category, question, expected_answer, context)
    VALUES (?, ?, ?, ?, ?)
    """
    return execute_commit(
        query, (dataset_id, category, question, expected_answer, context)
    )


def update_test_case(
    test_case_id: int,
    category: str,
    question: str,
    expected_answer: str,
    context: str,
):
    query = """
    UPDATE test_cases 
    SET category = ?, question = ?, expected_answer = ?, context = ?
    WHERE id = ?
    """
    execute_commit(
        query, (category, question, expected_answer, context, test_case_id)
    )


def delete_test_case(test_case_id: int):
    execute_commit("DELETE FROM test_cases WHERE id = ?", (test_case_id,))


def get_all_test_cases(dataset_id: Optional[int] = None) -> List[Dict[str, Any]]:
    if dataset_id:
        rows = execute_query(
            "SELECT * FROM test_cases WHERE dataset_id = ? ORDER BY id DESC",
            (dataset_id,),
        )
    else:
        rows = execute_query("SELECT * FROM test_cases ORDER BY id DESC")
    return [dict(r) for r in rows]


def create_evaluation_run(
    run_name: str, engine: str, model_name: str = "gpt-4o-mini"
) -> int:
    query = """
    INSERT INTO evaluation_runs (run_name, engine, model_name, status)
    VALUES (?, ?, ?, 'RUNNING')
    """
    return execute_commit(query, (run_name, engine, model_name))


def update_evaluation_run_summary(
    run_id: int, total_samples: int, overall_score: float, status: str = "COMPLETED"
):
    query = """
    UPDATE evaluation_runs 
    SET total_samples = ?, overall_score = ?, status = ?
    WHERE id = ?
    """
    execute_commit(query, (total_samples, overall_score, status, run_id))


def insert_evaluation_result(
    run_id: int,
    test_case_id: Optional[int],
    question: str,
    actual_response: str,
    expected_answer: str,
    context: str,
    metric_name: str,
    metric_score: float,
    passed: bool,
    reason: str,
) -> int:
    query = """
    INSERT INTO evaluation_results (
        run_id, test_case_id, question, actual_response, expected_answer,
        context, metric_name, metric_score, passed, reason
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    return execute_commit(
        query,
        (
            run_id,
            test_case_id,
            question,
            actual_response,
            expected_answer,
            context,
            metric_name,
            metric_score,
            1 if passed else 0,
            reason,
        ),
    )


def get_evaluation_runs() -> List[Dict[str, Any]]:
    rows = execute_query("SELECT * FROM evaluation_runs ORDER BY id DESC")
    return [dict(r) for r in rows]


def get_evaluation_results(run_id: Optional[int] = None) -> List[Dict[str, Any]]:
    if run_id:
        rows = execute_query(
            "SELECT * FROM evaluation_results WHERE run_id = ? ORDER BY id ASC",
            (run_id,),
        )
    else:
        rows = execute_query(
            "SELECT * FROM evaluation_results ORDER BY id DESC LIMIT 500"
        )
    return [dict(r) for r in rows]


def insert_regression_run(
    suite_name: str,
    baseline_run_id: int,
    candidate_run_id: int,
    baseline_score: float,
    candidate_score: float,
    score_delta: float,
    threshold: float,
    status: str,
    pytest_output: str,
) -> int:
    query = """
    INSERT INTO regression_runs (
        suite_name, baseline_run_id, candidate_run_id, baseline_score,
        candidate_score, score_delta, threshold, status, pytest_output
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    return execute_commit(
        query,
        (
            suite_name,
            baseline_run_id,
            candidate_run_id,
            baseline_score,
            candidate_score,
            score_delta,
            threshold,
            status,
            pytest_output,
        ),
    )


def get_regression_runs() -> List[Dict[str, Any]]:
    rows = execute_query("SELECT * FROM regression_runs ORDER BY id DESC")
    return [dict(r) for r in rows]


def insert_safety_test(
    category: str,
    attack_vector: str,
    prompt: str,
    model_response: str,
    is_safe: bool,
    severity: str,
    detection_reason: str,
) -> int:
    query = """
    INSERT INTO safety_tests (
        category, attack_vector, prompt, model_response, is_safe, severity, detection_reason
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    return execute_commit(
        query,
        (
            category,
            attack_vector,
            prompt,
            model_response,
            1 if is_safe else 0,
            severity,
            detection_reason,
        ),
    )


def get_safety_tests() -> List[Dict[str, Any]]:
    rows = execute_query("SELECT * FROM safety_tests ORDER BY id DESC")
    return [dict(r) for r in rows]


def insert_conversation_turn(
    session_id: str,
    turn_index: int,
    role: str,
    content: str,
    consistency_score: float,
    contradiction_detected: bool,
    context_loss_detected: bool,
    notes: str,
) -> int:
    query = """
    INSERT INTO conversation_tests (
        session_id, turn_index, role, content, consistency_score,
        contradiction_detected, context_loss_detected, notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    return execute_commit(
        query,
        (
            session_id,
            turn_index,
            role,
            content,
            consistency_score,
            1 if contradiction_detected else 0,
            1 if context_loss_detected else 0,
            notes,
        ),
    )


def get_conversation_history(session_id: str) -> List[Dict[str, Any]]:
    rows = execute_query(
        "SELECT * FROM conversation_tests WHERE session_id = ? ORDER BY turn_index ASC",
        (session_id,),
    )
    return [dict(r) for r in rows]


def get_all_conversation_sessions() -> List[str]:
    rows = execute_query(
        "SELECT DISTINCT session_id FROM conversation_tests ORDER BY created_at DESC"
    )
    return [r["session_id"] for r in rows]