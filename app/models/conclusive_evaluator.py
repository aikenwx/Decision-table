from app.models.abstract_evaluator import AbstractEvaluator
from app.models.decision_data_holder import DecisionDataHolder

# To keep track of which evaluator has the highest priority


class ConclusiveEvaluator(AbstractEvaluator):

    def __init__(self, key: str, status: str, priority: int) -> None:
        super(ConclusiveEvaluator, self).__init__(key, status)
        
        self.storage_key = "ConclusiveEvaluator_" + key + "_" + status
        self.priority = priority


    def evaluate(self, ddh: DecisionDataHolder) -> list:
        ddh.update_output_value(self)
        return []

    def has_higher_priority(self, other: "ConclusiveEvaluator") -> bool:
        return self.priority < other.priority

    def update_output_result(self, ddh: DecisionDataHolder) -> None:
        ddh[self.key] = self.value
    