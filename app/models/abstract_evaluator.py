from abc import ABC, abstractmethod
from app.models.decision_data_holder import DecisionDataHolder


class AbstractEvaluator(ABC):

    def __init__(self, key: str, value: str):
        if not key:
            raise ValueError("Key cannot be empty")

        if not value:
            raise ValueError("Value cannot be empty")
        self.next_evaluators = []
        self.next_evaluators_dict = {}
        self.key = key
        self.value = value
        self.storage_key = None

    # Updates the result of the evaluation if evaluation is complete or returns the next evaluator to be evaluated
    @abstractmethod
    def evaluate(self, ddh: DecisionDataHolder) -> list:
        raise NotImplementedError()

    # Adds the next evaluator to list of next evaluators
    def add_evaluator(self, next_evaluator: "AbstractEvaluator") -> "AbstractEvaluator":
        if (next_evaluator.get_storage_key() in self.next_evaluators_dict):
            stored_evaluator = self.next_evaluators_dict[next_evaluator.get_storage_key()]

            # transfer all evaluators from next_evaluator to stored_evaluator
            for evaluator in next_evaluator.get_all_evaluators():
                stored_evaluator.add_evaluator(evaluator)

            return stored_evaluator
        # not in next_evaluators_dict:
        else:
            self.next_evaluators_dict[next_evaluator.get_storage_key()] = next_evaluator
            self.next_evaluators.append(next_evaluator)

            return next_evaluator

    def get_all_evaluators(self) -> list:
        return self.next_evaluators

    def get_storage_key(self) -> str:
        if not self.storage_key:
            raise ValueError("Storage key not set")
        return self.storage_key
