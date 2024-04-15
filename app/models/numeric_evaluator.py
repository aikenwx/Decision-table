from app.models.abstract_evaluator import AbstractEvaluator
from app.models.decision_data_holder import DecisionDataHolder
import re


class NumericEvaluator(AbstractEvaluator):

    def __init__(self, key: str, result: str):

        # call the parent class constructor
        super(NumericEvaluator, self).__init__(key, result)

        match_string = r'[-]?\d+(?:\.\d+)?$'

        switch = {
            r'>=':  lambda num:lambda x: x >= num,
            r'<=':  lambda num:lambda x: x <= num,
            r'>': lambda num: lambda x: x > num,
            r'<': lambda num: lambda x: x < num,
            r'=': lambda num: lambda x: x == num
        }


        for switch_key, switch_value in switch.items():
            if re.search(r'^' + switch_key + match_string, result):
                num = float(result[len(switch_key):])
                self.eval_predicate = switch_value(num)
                self.storage_key = "NumericEvaluator_" + key + "_" + switch_key + str(num)
                return
       
        raise ValueError("Bad input for numeric evaluator.")

    def evaluate(self, ddh: DecisionDataHolder) -> list:
        if self.eval_predicate(ddh[self.key]):
            return self.get_all_evaluators()
        else:
            return []
