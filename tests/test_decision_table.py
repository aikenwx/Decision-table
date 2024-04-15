import pytest
from pathlib import Path
from app.models.decision_data_holder import DecisionDataHolder
from app.models.decision_table import DecisionTable


@pytest.fixture
def decision_table_nr1():
    return DecisionTable.create_from_csv(
        Path("tests/resources/decision_tables/scoring_process_result.csv")
    )

@pytest.fixture
def decision_table_nr2():
    return DecisionTable.create_from_csv(
        Path('tests/resources/decision_tables/test_input_2.csv')
    )


def test_rejected(decision_table_nr1):
    ddh = DecisionDataHolder({
        "hard_check_passed": False,
        "risk_score": 8,
        "all_data_collected": True
    })
    decision_table_nr1.evaluate(ddh)
    assert "status" in ddh
    assert ddh["status"] == "REJECTED"

    ddh["all_data_collected"] = False
    decision_table_nr1.evaluate(ddh)
    assert "status" in ddh
    assert ddh["status"] == "REJECTED"


def test_more_data(decision_table_nr1):
    ddh = DecisionDataHolder({
        "hard_check_passed": True,
        "risk_score": 8,
        "all_data_collected": False
    })
    decision_table_nr1.evaluate(ddh)
    assert "status" in ddh
    assert ddh["status"] == "MORE_DATA"


def test_approved(decision_table_nr1):
    ddh = DecisionDataHolder({
        "hard_check_passed": True,
        "risk_score": 12,
        "all_data_collected": True
    })
    decision_table_nr1.evaluate(ddh)
    assert "status" in ddh
    assert ddh["status"] == "APPROVED"


def test_no_row_matched(decision_table_nr1):
    ddh = DecisionDataHolder({
        "hard_check_passed": True,
        "risk_score": 9,
        "all_data_collected": True
    })
    decision_table_nr1.evaluate(ddh)
    assert "status" not in ddh

def test_row_of_higher_priority_matched(decision_table_nr2):
    ddh = DecisionDataHolder({
        "input1": 1,
        "input2": 3
    })
    decision_table_nr2.evaluate(ddh)
    assert "status" in ddh
    assert ddh["status"] == "OUTPUT2"

    ddh = DecisionDataHolder({
        "input1": 1,
        "input2": 0
    })

    # verify that 3rd row is matchable
    decision_table_nr2.evaluate(ddh)
    assert "status" in ddh
    assert ddh["status"] == "OUTPUT3"

