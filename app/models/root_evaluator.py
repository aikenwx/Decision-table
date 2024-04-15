from app.models.abstract_evaluator import AbstractEvaluator
from app.models.decision_data_holder import DecisionDataHolder


class RootEvaluator(AbstractEvaluator):
    def __init__(self):
        super(RootEvaluator, self).__init__("rootKey","rootValue")

    def evaluate(self, ddh: DecisionDataHolder) -> list:
        return self.get_all_evaluators()

    def get_storage_key(self) -> str:
        return "RootEvaluator"