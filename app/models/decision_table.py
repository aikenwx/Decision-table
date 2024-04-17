from app.models.abstract import AbstractDecisionTable
from pandas import read_csv, DataFrame
from app.models.evaluator_factory import EvaluatorFactory
from app.models.root_evaluator import RootEvaluator
from app.models.conclusive_evaluator import ConclusiveEvaluator
from collections import deque
from pathlib import Path
from app.models.decision_data_holder import DecisionDataHolder
import csv


class DecisionTable(AbstractDecisionTable):
    # accept pandas dataframe
    def __init__(self, arr_of_dict: list):
        # for each row in the dataframe
        self.root_evaluator = EvaluatorFactory().create_from_arr_of_dict(arr_of_dict)


    @staticmethod
    def create_from_csv(filepath: Path) -> "AbstractDecisionTable":
        with open(filepath, 'r') as file:
            reader = csv.reader(file, delimiter=';')  
            arr_of_dict = []
            keys = []

            for i, row in enumerate(reader):
                if (i == 0):
                    keys = row
                    continue
                
                dic = {}
                for i in range(0, len(keys)):
                    dic[keys[i]] = row[i]
                arr_of_dict.append(dic)
                
            return DecisionTable(arr_of_dict)

    def evaluate(self, ddh: DecisionDataHolder) -> bool:
        queue = deque()
        queue.append(self.root_evaluator)

        # BFS
        while len(queue) > 0:
            evaluator = queue.popleft()
            queue.extend(evaluator.evaluate(ddh))

        return False
