
from modules.conversation_testing import analyze_consistency


def test_no_contradiction():
    score, contradiction, notes = analyze_consistency(
        ["Java is an object-oriented programming language."],
        "Java supports classes and objects."
    )

    assert score == 100.0
    assert contradiction is False


def test_yes_no_contradiction():
    score, contradiction, notes = analyze_consistency(
        ["The answer is yes."],
        "The answer is no."
    )

    assert score == 40.0
    assert contradiction is True


def test_true_false_contradiction():
    score, contradiction, notes = analyze_consistency(
        ["The statement is true."],
        "The statement is false."
    )

    assert score == 40.0
    assert contradiction is True


def test_always_never_contradiction():
    score, contradiction, notes = analyze_consistency(
        ["This service is always available."],
        "This service is never available."
    )

    assert score == 40.0
    assert contradiction is True


def test_case_insensitive_contradiction():
    score, contradiction, notes = analyze_consistency(
        ["The system is SAFE."],
        "The system is UNSAFE."
    )

    assert score == 40.0
    assert contradiction is True
