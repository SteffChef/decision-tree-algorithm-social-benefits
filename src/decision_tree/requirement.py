from typing import List, Set, Dict, Tuple
from attribute import Attribute
from collections import Counter
import pandas as pd
import operator
from functools import reduce

class Requirement:
    """
    Base class for all requirement types, providing common properties and methods.
    """

    def __init__(self):
        self.is_relevant = True
        self.parent: 'Requirement' = None
        self.social_benefit = None
    
    def set_parent(self, parent: 'Requirement'):
        self.parent = parent

    def set_social_benefit(self, social_benefit):
        self.social_benefit = social_benefit

    def _update_relevant_attributes(self) -> None:
        """
        Updates relevant attributes and notifies the parent if present.
        """
        self.set_relevant_attributes()
        if self.parent is not None:
            self.parent.set_relevant_attributes()

class Requirement_Logical(Requirement):
    """
    Represents logical requirements (AND, OR) that contain other requirements.
    """

    def __init__(self, requirements: List[Requirement]) -> None:
        super().__init__()
        self.requirements = requirements
    
    def add_requirement(self, requirement: Requirement) -> None:
        """
        Adds a requirement to the list of requirements.

        Parameters:
        - requirement (Requirement): The requirement to add.
        """

        self.requirements.append(requirement)
        self._update_relevant_attributes()
        print(f"Requirement {requirement.get_tree_string()} successfully added.")
    
    def reset_evaluations(self) -> None:
        """
        Resets evaluation results for the requirement and all its child requirements.
        """

        self.is_relevant = True
        for requirement in self.requirements:
            requirement.reset_evaluations()

    def remove_requirement(self, requirement: Requirement) -> None:
        """
        Removes a requirement from the list of requirements.

        Parameters:
        - requirement (Requirement): The requirement to remove.
        """

        try:
            self.requirements.remove(requirement)
            self._update_relevant_attributes()
            print(f"Requirement {requirement.get_tree_string()} successfully removed.")
        except ValueError:
            print(f"Requirement not found and cannot be removed.")

    def remove_requirement_by_attribute(self, attribute: Attribute) -> None:
        """
        Removes a requirement from the list of requirements.

        Parameters:
        - requirement (Requirement): The requirement to remove.
        """

        to_remove = None
        for requirement in self.requirements:
            if isinstance(requirement, Requirement_Concrete) and requirement.attribute == attribute:
                to_remove = requirement
                break
            else:
                requirement.remove_requirement_by_attribute(attribute)
                
        if to_remove:
            self.remove_requirement(to_remove)

class Logical_AND(Requirement_Logical):

    """
    Represents a logical AND requirement. It evaluates to True if all its child requirements
    evaluate to True given a set of data. This class extends Requirement_Logical, inheriting
    its structure and behaviors but specifies evaluation logic specific to the AND operation.
    """

    def evaluate(self, data: Dict) -> bool:
        """
        Evaluates the logical AND condition across all child requirements using the given data.

        Parameters:
        - data (Dict): A dictionary of data used to evaluate each requirement.

        Returns:
        - bool: True if all child requirements evaluate to True, False otherwise.
        """

        # If no relevant attributes are present, the requirement is always true
        if not any(key in self.relevant_attributes for key in data.keys()):
            return True

        # Evaluate each requirement, return False if any do not meet the condition
        for requirement in self.requirements:
            if not requirement.evaluate(data):
                self.is_relevant = False
                return False
        
        self.set_relevant_attributes()
        return True
    
    def get_relevant_attribute_counts(self) -> Tuple[Counter,int]:

        """
        Calculates the count of relevant attributes and the constellation count among all child requirements.

        Returns:
        - Tuple[Counter, int]: A tuple containing a Counter of attributes and their counts, and the constellation count.
        """

        constellation_count = 1
        attribute_counts = Counter()


        for requirement in self.requirements:
            if requirement.is_relevant:
                req_attribute_counts, req_constellation_count = requirement.get_relevant_attribute_counts()
                constellation_count *= req_constellation_count
                scaled_counts = {e: count * (constellation_count // req_constellation_count) for e, count in req_attribute_counts.items()}
                attribute_counts.update(scaled_counts)

        return attribute_counts, constellation_count
        
    def get_tree_string(self) -> str:
        return 'AND'
    
    def export(self) -> Dict:
        return {
            'type': 'AND',
            'content': [requirement.export() for requirement in self.requirements]
        }
    
    def get_dataframe(self) -> pd.DataFrame:

        dataframes = [requirement.get_dataframe() for requirement in self.requirements]
        constellations = reduce(operator.mul,(len(dataframe) for dataframe in dataframes))

        adjusted_dataframes = [pd.concat([dataframe]*(constellations // len(dataframe)), ignore_index=True) for dataframe in dataframes]
        return pd.concat(adjusted_dataframes, axis=1)

class Logical_OR(Requirement_Logical):
    
    # should one requirement be true, the whole requirement is true, otherwise false
    def evaluate(self, data: Dict) -> bool:
        if any(key in self.relevant_attributes for key in data.keys()):
            for requirement in self.requirements:
                if requirement.evaluate(data):
                    self.is_relevant = False
                    return True
            return False
        else:
            return True
        
    def get_relevant_attribute_counts(self) -> Set[str]:
        constellation_count = 0
        attribute_counts = Counter()
        for requirement in self.requirements:
            # find new Constellation Count
            if requirement.is_relevant:
                req_attribute_counts, req_constellation_count = requirement.get_relevant_attribute_counts()
                attribute_counts += req_attribute_counts
                constellation_count += req_constellation_count
        return attribute_counts, constellation_count
    
    def get_dataframe(self) -> pd.DataFrame:

        dataframes = [requirement.get_dataframe() for requirement in self.requirements]
        return pd.concat(dataframes, ignore_index=True)
        
    def get_tree_string(self) -> str:
        return 'OR'
    
    def export(self) -> Dict:
        return {
            'type': 'OR',
            'content': [requirement.export() for requirement in self.requirements]
        }
    
class Requirement_Concrete(Requirement):

    def __init__(self, attribute: Attribute):
        super().__init__()
        self.attribute = attribute

    
    def get_relevant_attribute_counts(self) -> tuple[Counter,int]:
        return Counter({self.attribute.title:1}),1
    
    def reset_evaluations(self):
        self.is_relevant = True


class Requirement_Numerical(Requirement_Concrete):

    comparison_operators = ['<=','>=','==','[]']

    def __init__(self,  attribute: Attribute, comparison_operator: str, required_value: List[int]):
        super().__init__(attribute=attribute)
        self.comparison_operator = comparison_operator
        self.required_value = required_value

    def set_comparison_operator(self, comparison_operator: str):
        if comparison_operator in self.comparison_operators:
            self.comparison_operator = comparison_operator
        else:
            print(f"Invalid comparison operator {comparison_operator}.")


    def evaluate(self,data) -> bool:
    # Check if the key exists in data and get the value; return True if the key doesn't exist
        value = data.get(self.attribute.title)
        if value is None:
            return True

        self.is_relevant = False  # Assuming you want to mark as not relevant when the key exists

        # Define comparison operations in a dictionary
        operations = {
            '<': lambda x: x < self.required_value[0],
            '<=': lambda x: x <= self.required_value[0],
            '>': lambda x: x > self.required_value[0],
            '>=': lambda x: x >= self.required_value[0],
            '==': lambda x: x == self.required_value[0],
            '[]': lambda x: self.required_value[0] <= x <= self.required_value[1],
        }

        # Get the comparison function from the dictionary and apply it
        compare = operations.get(self.comparison_operator, lambda x: True)
        return compare(value)
        
    def get_tree_string(self) -> str:
        return f'{self.attribute.title} {self.comparison_operator} {self.required_value}'
    
    def export(self) -> Dict:
        return {
            'type': 'attribute_numerical',
            'content': {
                'title': self.attribute.title,
                'comparison_operator': self.comparison_operator,
                'required_value': self.required_value
            }
        }
    
    def get_dataframe(self) -> pd.DataFrame:
        if self.comparison_operator == '[]':
            return pd.DataFrame({self.attribute.title: [(self.required_value[0],self.required_value[1])]})
        if self.comparison_operator == '==':
            return pd.DataFrame({self.attribute.title: [(self.required_value[0],self.required_value[0])]})
        if self.comparison_operator == '<=':
            return pd.DataFrame({self.attribute.title: [(self.attribute.min,self.required_value[0])]})
        if self.comparison_operator == '>=':
            return pd.DataFrame({self.attribute.title: [(self.required_value[0],self.attribute.max)]})

class Requirement_Categorical(Requirement_Concrete):

    def __init__(self, attribute: Attribute, required_value: List[str]):
        super().__init__(attribute=attribute)
        self.required_value = required_value

    def evaluate(self,data) -> bool:
        if any(key == self.attribute.title for key in data.keys()):
            self.is_relevant = False
            return data[self.attribute.title] in self.required_value
        else:
            return True
        
    def get_tree_string(self) -> str:
        return f'{self.attribute.title} in {self.required_value}'
    
    def get_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame({self.attribute.title: [f'{required_value}' for required_value in self.required_value]})
    
    def export(self) -> Dict:
        return {
            'type': 'attribute_categorical',
            'content': {
                'title': self.attribute.title,
                'required_value': self.required_value
            }
        }