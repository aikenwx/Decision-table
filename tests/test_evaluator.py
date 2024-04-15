import pytest
from pathlib import Path
from app.models.decision_data_holder import DecisionDataHolder
from app.models.decision_table import DecisionTable
from app.models.root_evaluator import RootEvaluator
from app.models.boolean_evaluator import BooleanEvaluator
from app.models.numeric_evaluator import NumericEvaluator
from app.models.conclusive_evaluator import ConclusiveEvaluator



def test_numeric_evaluator_should_not_recognize_invalid_input():
    try:
        NumericEvaluator("numericKey", "invalid input")
    except ValueError as e:
        assert e.args[0] == "Bad input for numeric evaluator."
    else:
        assert False

    try:
        NumericEvaluator("numericKey", "==10.0")
    except ValueError as e:
        assert e.args[0] == "Bad input for numeric evaluator."
    else:
        assert False

    try:
        NumericEvaluator("numericKey", "=>10.0")
    except ValueError as e:
        assert e.args[0] == "Bad input for numeric evaluator."
    else:
        assert False

    
    try:
        NumericEvaluator("numericKey", "10.0")
    except ValueError as e:
        assert e.args[0] == "Bad input for numeric evaluator."
    else:
        assert False
    

def test_evaluate_gt_numeric_should_evaluate_correctly():
    numeric_evaluator = NumericEvaluator("numericKey", ">10.0")
    conclusive_evaluator = ConclusiveEvaluator("conclusiveKey", "conclusiveValue", 0)
    numeric_evaluator.add_evaluator(conclusive_evaluator)

    assert len(numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 11}))) == 1
    assert numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 11}))[0] == conclusive_evaluator
    assert len(numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 10.0001}))) == 1
    assert numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 10.0001}))[0] == conclusive_evaluator
    assert len(numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 10}))) == 0
    assert len(numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 9.0}))) == 0



def test_evaluate_lt_numeric_should_evaluate_correctly():
    numeric_evaluator = NumericEvaluator("numericKey", "<10.0")
    conclusive_evaluator = ConclusiveEvaluator("conclusiveKey", "conclusiveValue", 0)
    numeric_evaluator.add_evaluator(conclusive_evaluator)

    assert len(numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 9}))) == 1
    assert numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 9}))[0] == conclusive_evaluator
    assert len(numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 9.9999}))) == 1
    assert numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 9.9999}))[0] == conclusive_evaluator
    assert len(numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 10}))) == 0
    assert len(numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 11.0}))) == 0
    

def test_evaluate_eq_numeric_should_evaluate_correctly():
    numeric_evaluator = NumericEvaluator("numericKey", "=10.0")
    conclusive_evaluator = ConclusiveEvaluator("conclusiveKey", "conclusiveValue", 0)
    numeric_evaluator.add_evaluator(conclusive_evaluator)

    assert len(numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 10}))) == 1
    assert numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 10}))[0] == conclusive_evaluator
    assert len(numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 10.0}))) == 1
    assert numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 10.0}))[0] == conclusive_evaluator
    assert len(numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 9.9999}))) == 0
    assert len(numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 11.0}))) == 0

def test_evaluate_gte_numeric_should_evaluate_correctly():
    numeric_evaluator = NumericEvaluator("numericKey", ">=10.0")
    conclusive_evaluator = ConclusiveEvaluator("conclusiveKey", "conclusiveValue", 0)
    numeric_evaluator.add_evaluator(conclusive_evaluator)

    assert len(numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 11}))) == 1
    assert numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 11}))[0] == conclusive_evaluator
    assert len(numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 10.0001}))) == 1
    assert numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 10.0001}))[0] == conclusive_evaluator
    assert len(numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 10}))) == 1
    assert numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 10}))[0] == conclusive_evaluator
    assert len(numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 9.0}))) == 0

def test_evaluate_lte_numeric_should_evaluate_correctly():
    numeric_evaluator = NumericEvaluator("numericKey", "<=10.0")
    conclusive_evaluator = ConclusiveEvaluator("conclusiveKey", "conclusiveValue", 0)
    numeric_evaluator.add_evaluator(conclusive_evaluator)

    assert len(numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 9}))) == 1
    assert numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 9}))[0] == conclusive_evaluator

    assert len(numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 9.9999}))) == 1
    assert numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 9.9999}))[0] == conclusive_evaluator

    assert len(numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 10}))) == 1
    assert numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 10}))[0] == conclusive_evaluator

    assert len(numeric_evaluator.evaluate(DecisionDataHolder({"numericKey": 11.0}))) == 0

def test_root_evaluator_should_return_all_evaluators():
    root_evaluator = RootEvaluator()
    boolean_evaluator = BooleanEvaluator("booleanKey", "=True")
    numeric_evaluator = NumericEvaluator("numericKey", ">10.0")
    conclusive_evaluator = ConclusiveEvaluator("conclusiveKey", "conclusiveValue", 0)

    root_evaluator.add_evaluator(boolean_evaluator)
    root_evaluator.add_evaluator(numeric_evaluator)
    root_evaluator.add_evaluator(conclusive_evaluator)
    # test duplicate
    root_evaluator.add_evaluator(conclusive_evaluator)

    assert len(root_evaluator.evaluate(DecisionDataHolder({"booleanKey": True, "numericKey": 11}))) == 3
    assert root_evaluator.evaluate(DecisionDataHolder({"booleanKey": True, "numericKey": 11}))[0] == boolean_evaluator
    assert root_evaluator.evaluate(DecisionDataHolder({"booleanKey": True, "numericKey": 11}))[1] == numeric_evaluator
    assert root_evaluator.evaluate(DecisionDataHolder({"booleanKey": True, "numericKey": 11}))[2] == conclusive_evaluator

def test_conclusive_evaluator_should_update_decision_data_holder():
    conclusive_evaluator = ConclusiveEvaluator("conclusiveKey", "conclusiveValue", 0)
    ddh = DecisionDataHolder({})
    assert len(conclusive_evaluator.evaluate(ddh)) == 0
    assert ddh["conclusiveKey"] == "conclusiveValue"


def create_evaluator():
    boolean_evaluator = BooleanEvaluator("booleanKey", "=True")
    numeric_evaluator = NumericEvaluator("numericKey", ">10.0")
    conclusive_evaluator = ConclusiveEvaluator("conclusiveKey", "conclusiveValue", 0)

    boolean_evaluator.add_evaluator(numeric_evaluator)
    numeric_evaluator.add_evaluator(conclusive_evaluator)
    return boolean_evaluator


def create_evaluator2():
    boolean_evaluator = BooleanEvaluator("booleanKey", "=True")
    numeric_evaluator = NumericEvaluator("numericKey", "=10.0")
    conclusive_evaluator = ConclusiveEvaluator("conclusiveKey", "conclusiveValue", 0)

    boolean_evaluator.add_evaluator(numeric_evaluator)
    numeric_evaluator.add_evaluator(conclusive_evaluator)
    return boolean_evaluator


def test_adding_duplicate_evaluator_should_remove_duplicates_from_list():
    boolean_evaluator = BooleanEvaluator("booleanKey", "=True")
    boolean_evaluator2 = BooleanEvaluator("booleanKey", "=True")

    root_evaluator = RootEvaluator()
    root_evaluator.add_evaluator(boolean_evaluator)
    assert len(root_evaluator.get_all_evaluators()) == 1
    assert root_evaluator.get_all_evaluators()[0].get_storage_key() == "BooleanEvaluator_booleanKey_True" 

    root_evaluator.add_evaluator(boolean_evaluator2)
    assert len(root_evaluator.get_all_evaluators()) == 1
    assert root_evaluator.get_all_evaluators()[0].get_storage_key() == "BooleanEvaluator_booleanKey_True"

def test_adding_distinct_evaluator_should_return_list_of_distinct_evaluators():
    numeric_evaluator = NumericEvaluator("numericKey", ">10.0")
    numeric_evaluator2 = NumericEvaluator("numericKey", "=10.0")
    numeric_evaluator3 = NumericEvaluator("numericKey", "<10.0")
    numeric_evaluator4 = NumericEvaluator("numericKey", "=10.0")

    root_evaluator = RootEvaluator()

    root_evaluator.add_evaluator(numeric_evaluator)
    assert len(root_evaluator.get_all_evaluators()) == 1
    assert root_evaluator.get_all_evaluators()[0].get_storage_key() == "NumericEvaluator_numericKey_>10.0"

    root_evaluator.add_evaluator(numeric_evaluator2)
    assert len(root_evaluator.get_all_evaluators()) == 2
    assert root_evaluator.get_all_evaluators()[1].get_storage_key() == "NumericEvaluator_numericKey_=10.0"

    root_evaluator.add_evaluator(numeric_evaluator3)
    assert len(root_evaluator.get_all_evaluators()) == 3
    assert root_evaluator.get_all_evaluators()[2].get_storage_key() == "NumericEvaluator_numericKey_<10.0"

    root_evaluator.add_evaluator(numeric_evaluator4)
    assert len(root_evaluator.get_all_evaluators()) == 3


def test_adding_nested_duplicate_evaluator_should_remove_nested_duplicates():
    root_evaluator = RootEvaluator()
    root_evaluator.add_evaluator(create_evaluator())
    root_evaluator.add_evaluator(create_evaluator())

    assert len(root_evaluator.get_all_evaluators()) == 1
    assert root_evaluator.get_all_evaluators()[0].get_storage_key() == "BooleanEvaluator_booleanKey_True"
    assert len(root_evaluator.get_all_evaluators()[0].next_evaluators) == 1
    assert root_evaluator.get_all_evaluators()[0].next_evaluators[0].get_storage_key() == "NumericEvaluator_numericKey_>10.0"
    assert len(root_evaluator.get_all_evaluators()[0].next_evaluators[0].next_evaluators) == 1
    assert root_evaluator.get_all_evaluators()[0].next_evaluators[0].next_evaluators[0].get_storage_key(
    ) == "ConclusiveEvaluator_conclusiveKey_conclusiveValue"

    root_evaluator.add_evaluator(create_evaluator2())
    assert len(root_evaluator.get_all_evaluators()) == 1
    assert root_evaluator.get_all_evaluators()[0].get_storage_key() == "BooleanEvaluator_booleanKey_True"
    assert len(root_evaluator.get_all_evaluators()[0].next_evaluators) == 2
    assert root_evaluator.get_all_evaluators()[0].next_evaluators[0].get_storage_key() == "NumericEvaluator_numericKey_>10.0"
    assert root_evaluator.get_all_evaluators()[0].next_evaluators[1].get_storage_key() == "NumericEvaluator_numericKey_=10.0"

    assert len(root_evaluator.get_all_evaluators()[0].next_evaluators[0].next_evaluators) == 1
    assert len(root_evaluator.get_all_evaluators()[0].next_evaluators[1].next_evaluators) == 1

    assert root_evaluator.get_all_evaluators()[0].next_evaluators[0].next_evaluators[0].get_storage_key(
    ) == "ConclusiveEvaluator_conclusiveKey_conclusiveValue"
    assert root_evaluator.get_all_evaluators()[0].next_evaluators[1].next_evaluators[0].get_storage_key(
    ) == "ConclusiveEvaluator_conclusiveKey_conclusiveValue"

def test_stuff():
    decision_data_holder = DecisionDataHolder({"booleanKey": True, "numericKey": 11})