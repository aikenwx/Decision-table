from app.models.abstract_evaluator import AbstractEvaluator
from app.models.decision_data_holder import DecisionDataHolder


class BooleanEvaluator(AbstractEvaluator):

    def __init__(self, key: str, result: str):

        # call the parent class constructor
        super(BooleanEvaluator, self).__init__(key, result)

        if result not in ['=True', '=False', '=true', '=false']:
            raise ValueError("Bad input for boolean evaluator.")

        if result == '=True' or result == '=true':
            self.result = True
        else:
            self.result = False

        self.storage_key = "BooleanEvaluator_" + key + "_" + str(self.result)

        

    def evaluate(self, ddh: DecisionDataHolder) -> list:
        if ddh[self.key] == self.result:
            return self.get_all_evaluators()
        else:
            return []

