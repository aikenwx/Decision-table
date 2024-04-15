from app.models.abstract import AbstractDecisionTable
from pandas import read_csv, DataFrame
from app.models.evaluator_factory import EvaluatorFactory
from app.models.root_evaluator import RootEvaluator
from app.models.conclusive_evaluator import ConclusiveEvaluator
from collections import deque
from pathlib import Path
from app.models.decision_data_holder import DecisionDataHolder



class DecisionTable(AbstractDecisionTable):
    # accept pandas dataframe
    def __init__(self, dataframe: DataFrame):
        # for each row in the dataframe
        self.root_evaluator = EvaluatorFactory().create_from_dataframe(dataframe)


    @staticmethod
    def create_from_csv(filepath: Path) -> "AbstractDecisionTable":
        # parse the CSV file into a dictionary
        df = read_csv(filepath, delimiter=';')
        return DecisionTable(df)


    def evaluate(self, ddh: DecisionDataHolder) -> bool:
        queue = deque()
        queue.append(self.root_evaluator)

        # BFS
        while len(queue) > 0:
            evaluator = queue.popleft()
            queue.extend(evaluator.evaluate(ddh))

        return False
