from app.models.boolean_evaluator import BooleanEvaluator
from app.models.numeric_evaluator import NumericEvaluator
from app.models.abstract_evaluator import AbstractEvaluator
from app.models.root_evaluator import RootEvaluator
from app.models.conclusive_evaluator import ConclusiveEvaluator
from pandas import DataFrame

INPUT_EVALUATORS = {
    "BooleanEvaluator": BooleanEvaluator,
    "NumericEvaluator": NumericEvaluator
}


# This class is responsible for parsing the input data and creating the appropriate evaluators.
# Should a new evaluator type be added, the INPUT_EVALUATORS should be updated to include the new type.
class EvaluatorFactory:

    def __init__(self):
        self.input_keys = None
        self.output_key = None
        

    def create(self, key: str, value: str) -> AbstractEvaluator:

        for _, evaluator in INPUT_EVALUATORS.items():
            try:
                evaluator = evaluator(key, value)
                return evaluator
            except ValueError:
                pass

        raise ValueError("Bad input for evaluator creation.")
    

    def create_from_row(self, input_row: dict, row_number: int) -> AbstractEvaluator:

        if self.input_keys is None or self.output_key is None:
            self.calculate_and_set_optimized_order(input_row)
        
        prev_evaluator = None
        first_evaluator = None
        for key in self.input_keys:
            value = input_row[key]
            
            evaluator = self.create(key, value)

            
            if prev_evaluator == None:
                first_evaluator = evaluator
            else:
                prev_evaluator.add_evaluator(evaluator)
            
            prev_evaluator = evaluator
        
        output_value = input_row[self.output_key]
        prev_evaluator.add_evaluator(ConclusiveEvaluator(self.output_key, output_value, row_number))
        
        return first_evaluator
        
    def create_from_dataframe(self, dataframe: DataFrame) -> AbstractEvaluator:
        root_evaluator = RootEvaluator()

        for index, row in dataframe.iterrows():
            dic = row.to_dict()

            evaluator = self.create_from_row(dic, index)
            root_evaluator.add_evaluator(evaluator)

        return root_evaluator


    # This method is responsible for setting the order of the evaluators in the decision table.
    # By evaluating evaluators like boolean evaluators first, where only one branch will be explored,
    # We can cut down on the number of evaluations needed to reach a conclusion.
    def calculate_and_set_optimized_order(self, input_row: dict):
        self.evaluator_keys_by_type = {}
        for evaluator_type in INPUT_EVALUATORS.keys():
            self.evaluator_keys_by_type[evaluator_type] = []

        self.output_key = None
        should_set_output_key = False


        for key, value in input_row.items():

            is_key_added = False

            for evaluator_type, evaluator in INPUT_EVALUATORS.items():
                try:
                    evaluator = evaluator(key, value)
                    self.evaluator_keys_by_type[evaluator_type].append(key)
                    is_key_added = True
                    break
                except ValueError:
                    pass
            if is_key_added:
                continue
            elif key == "*":
                should_set_output_key = True
                continue
            elif should_set_output_key:
                if self.output_key is not None:
                    raise ValueError("More than one output column specified")
                self.output_key = key
                continue

            else:
                raise ValueError("Unknown evaluator type")

        self.input_keys = []
        for keys in self.evaluator_keys_by_type.values():
            self.input_keys.extend(keys)
