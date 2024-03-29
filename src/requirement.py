from typing import List, Set, Dict, Tuple
from src.attribute import Attribute
from collections import Counter
import pandas as pd
import operator
from functools import reduce

class Requirement:
    """
    Base class for all requirement types, providing common properties and methods.
    """

    def __init__(self):
        self.parent: 'Requirement' = None
        self.social_benefit = None
    
    def set_parent(self, parent: 'Requirement'):
        self.parent = parent

    def set_social_benefit(self, social_benefit):
        self.social_benefit = social_benefit

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
        
    def get_tree_string(self) -> str:
        '''
        Returns a string representation of the requirement.

        Returns:
        str: A string representation of the requirement.
        
        '''
        return 'AND'
    
    def export(self) -> Dict:

        '''
        Exports the requirement as a dictionary.

        Returns:
        A dictionary representing the requirement with its type and content.
        
        '''
        return {
            'type': 'AND',
            'content': [requirement.export() for requirement in self.requirements]
        }
    
    def get_dataframe(self) -> pd.DataFrame:

        '''
        Returns the requirement as a dataframe.

        Returns:
        DataFrame: A dataframe representing the requirement.
        '''

        # we get the dataframes for each requirement and concatenate them
        dataframes = [requirement.get_dataframe() for requirement in self.requirements]
        constellations = reduce(operator.mul,(len(dataframe) for dataframe in dataframes))

        # dataframes are concatenated to match the length of the new dataframe
        adjusted_dataframes = [pd.concat([dataframe]*(constellations // len(dataframe)), ignore_index=True) for dataframe in dataframes]
        return pd.concat(adjusted_dataframes, axis=1)

class Logical_OR(Requirement_Logical):
    
    '''
    Represents a logical OR requirement. It evaluates to True if any of its child requirements
    evaluate to True given a set of data. This class extends Requirement_Logical, inheriting
    its structure and behaviors but specifies evaluation logic specific to the OR operation.
    '''
    
    def get_dataframe(self) -> pd.DataFrame:

        '''
        Returns the requirement as a dataframe.

        Returns:
        DataFrame: A dataframe representing the requirement.
        '''

        dataframes = [requirement.get_dataframe() for requirement in self.requirements]
        return pd.concat(dataframes, ignore_index=True)
        
    def get_tree_string(self) -> str:
        '''
        Returns a string representation of the requirement.

        Returns:
        str: A string representation of the requirement.
        
        '''
        return 'OR'
    
    def export(self) -> Dict:
        '''
        Exports the requirement as a dictionary.

        Returns:
        A dictionary representing the requirement with its type and content.
        
        '''
        return {
            'type': 'OR',
            'content': [requirement.export() for requirement in self.requirements]
        }
    
class Requirement_Concrete(Requirement):

    def __init__(self, attribute: Attribute):
        super().__init__()
        self.attribute = attribute


class Requirement_Numerical(Requirement_Concrete):

    comparison_operators = ['<=','>=','==','[]']

    def __init__(self,  attribute: Attribute, comparison_operator: str, required_value: List[int]):

        '''
        Initializes the Requirement_Numerical object with an attribute, comparison operator, and required value.

        Parameters:
        - attribute (Attribute): The attribute for the requirement.
        - comparison_operator (str): The comparison operator for the requirement.
        - required_value (List[int]): The required value for the requirement.

        '''
        super().__init__(attribute=attribute)
        self.comparison_operator = comparison_operator
        self.required_value = required_value

    def set_comparison_operator(self, comparison_operator: str):
        '''
        Sets the comparison operator for the requirement.

        Parameters:
        - comparison_operator (str): The comparison operator to set for the requirement.
        '''
        if comparison_operator in self.comparison_operators:
            self.comparison_operator = comparison_operator
        else:
            print(f"Invalid comparison operator {comparison_operator}.")

        
    def get_tree_string(self) -> str:
        '''
        Returns a string representation of the requirement.

        Returns:
        str: A string representation of the requirement.
        
        '''

        return f'{self.attribute.title} {self.comparison_operator} {self.required_value}'
    
    def export(self) -> Dict:

        '''
        Exports the requirement as a dictionary.

        '''
        return {
            'type': 'attribute_numerical',
            'content': {
                'title': self.attribute.title,
                'comparison_operator': self.comparison_operator,
                'required_value': self.required_value
            }
        }
    
    def get_dataframe(self) -> pd.DataFrame:
        '''
        Returns the requirement as a dataframe.

        Returns:
        DataFrame: A dataframe representing the requirement.
        '''

        # depending on the comparison operator, we return a dataframe with the required value
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

        
    def get_tree_string(self) -> str:
        '''
        Returns a string representation of the requirement.

        Returns:
        str: A string representation of the requirement.
        
        '''        
        return f'{self.attribute.title} in {self.required_value}'
    
    def get_dataframe(self) -> pd.DataFrame:
        '''
        Returns the requirement as a dataframe.

        Returns:
        DataFrame: A dataframe representing the requirement.
        '''
        return pd.DataFrame({self.attribute.title: [f'{required_value}' for required_value in self.required_value]})
    
    def export(self) -> Dict:
        '''
        Exports the requirement as a dictionary.

        Returns:
        A dictionary representing the requirement with its type, title, and required value.
        
        '''
        return {
            'type': 'attribute_categorical',
            'content': {
                'title': self.attribute.title,
                'required_value': self.required_value
            }
        }