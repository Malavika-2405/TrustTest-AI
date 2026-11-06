
from modules.semantic_evaluator import calculate_semantic_similarity


def test_identical_answers():
    score = calculate_semantic_similarity(
        "Java is an object-oriented programming language.",
        "Java is an object-oriented programming language."
    )

    assert score >= 95


def test_similar_meaning_answers():
    score = calculate_semantic_similarity(
        "Java is an object-oriented programming language.",
        "Java supports object-oriented programming."
    )

    assert score >= 70


def test_unrelated_answers():
    score = calculate_semantic_similarity(
        "Java is a programming language.",
        "The weather is sunny today."
    )

    assert score < 70


def test_empty_expected_answer():
    score = calculate_semantic_similarity("", "Java is a programming language.")

    assert score == 0.0


def test_empty_actual_answer():
    score = calculate_semantic_similarity("Java is a programming language.", "")

    assert score == 0.0