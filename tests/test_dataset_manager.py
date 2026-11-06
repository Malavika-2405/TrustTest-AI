
import pytest
import database.db as db


@pytest.fixture
def temporary_database(tmp_path, monkeypatch):
    test_db_path = tmp_path / "test_trusttest.db"

    monkeypatch.setattr(db, "DB_FILE", str(test_db_path))

    db.init_db()

    return test_db_path


def test_create_dataset(temporary_database):
    dataset_id = db.create_dataset(
        "Test Dataset",
        "Temporary dataset for automated testing"
    )

    assert dataset_id > 0

    datasets = db.get_all_datasets()

    assert len(datasets) == 1
    assert datasets[0]["name"] == "Test Dataset"


def test_retrieve_datasets(temporary_database):
    db.create_dataset("Dataset One", "First dataset")
    db.create_dataset("Dataset Two", "Second dataset")

    datasets = db.get_all_datasets()

    names = [dataset["name"] for dataset in datasets]

    assert "Dataset One" in names
    assert "Dataset Two" in names
    assert len(datasets) == 2


def test_insert_test_case(temporary_database):
    dataset_id = db.create_dataset("Java Dataset")

    case_id = db.insert_test_case(
        dataset_id,
        "General",
        "What is Java?",
        "Java is a programming language.",
        "Java reference context"
    )

    assert case_id > 0

    cases = db.get_all_test_cases(dataset_id)

    assert len(cases) == 1
    assert cases[0]["question"] == "What is Java?"


def test_update_test_case(temporary_database):
    dataset_id = db.create_dataset("Update Dataset")

    case_id = db.insert_test_case(
        dataset_id,
        "General",
        "Original question",
        "Original answer",
        ""
    )

    db.update_test_case(
        case_id,
        "Accuracy",
        "Updated question",
        "Updated answer",
        "Updated context"
    )

    cases = db.get_all_test_cases(dataset_id)

    assert cases[0]["category"] == "Accuracy"
    assert cases[0]["question"] == "Updated question"
    assert cases[0]["expected_answer"] == "Updated answer"
    assert cases[0]["context"] == "Updated context"


def test_delete_test_case(temporary_database):
    dataset_id = db.create_dataset("Delete Dataset")

    case_id = db.insert_test_case(
        dataset_id,
        "General",
        "Temporary question",
        "Temporary answer",
        ""
    )

    db.delete_test_case(case_id)

    cases = db.get_all_test_cases(dataset_id)

    assert len(cases) == 0
