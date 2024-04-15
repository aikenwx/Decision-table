##  Setup Instructions
1. pipenv shell
2. pipenv install
3. pytest

## Design

### Class Diagram
![Class Diagram](./decision_table_class_diagram.svg)

### Extendibility/ OCP
* The solution can be easily extended to support making decisions for different types of data by extending from the AbstractEvaluator class. 
* For example, a new CategoricalEvaluator class can be created to allow decisions to be made on categorical data. The new class would only need to implement the `evaluate` method. This follows the Open/Closed Principle.

### Factory Method
* The Factory Method pattern is used to create the Evaluator objects for the DecisionTable. 
* The EvaluatorFactory class is responsible for creating the appropriate Evaluator object based on the data type. 
* This reduces the coupling between the DecisionTable class and the Evaluator classes that handle input data. This follows the Dependency Inversion Principle. 
* However, adding new Evaluator classes would require small changes to the EvaluatorFactory class. This modification will be small, requiring only changes to the INPUT_EVALUATORS dictionary.

### DRY Principle
* The Evaluator classes are designed to be reusable and follow the DRY principle.
* Smart use of inheritance and composition (`AbstractEvaluator`) is used to avoid code duplication.
* In the factory class, the `INPUT_EVALUATORS` dictionary and a for loop is used to avoid code duplication for conditional checks when creating Evaluator objects.
* The above is also true for the `NumericEvaluator` class, which can match up to 5 different types of numeric conditions.

### Recursive/Tree-like Structure
* Each condition in the DecisionTable is represented as a node as an `AbstractEvaluator` in a tree-like structure.
* Each node is responsible for evaluating and deciding whether to traverse to the next nodes based on the input data.
* This allows us to use BFS traversal to solve the decision-making problem.

### Optimization
* Duplicate conditions are combined to reduce the number of comparisons required to make a decision. This is done by consolidating conditions that have the same predicate, forming a tree-like structure.
* Indexing on boolean values before numeric values is used to optimize the decision-making process. This is because decisions based on boolean values result in further evaluating one possible outcome branch (True or False). Whereas decisions based on numeric values may result in evaluating multiple outcome branches (e.g. input of 10 passes multiple conditions for <= 10, <20, <30, etc.).
* Hashtables are used to store and build the tree structure using evaluator classes, ensuring that duplicate evaluators can be efficiently identified and consolidated.


