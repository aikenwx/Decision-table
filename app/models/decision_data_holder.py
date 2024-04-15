import collections

class DecisionDataHolder(collections.UserDict):
    
    def __init__(self, *args, **kwargs):
        super(DecisionDataHolder, self).__init__(*args, **kwargs)
        self.last_conclusive_evaluator = None


    def update_output_value(self, conclusive_evaluator):
        if self.last_conclusive_evaluator is None:
            conclusive_evaluator.update_output_result(self)
            self.last_conclusive_evaluator = conclusive_evaluator
        elif conclusive_evaluator.has_higher_priority(self.last_conclusive_evaluator):
            conclusive_evaluator.update_output_result(self)
            self.last_conclusive_evaluator = conclusive_evaluator
            