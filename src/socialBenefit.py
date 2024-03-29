from typing import List, Set
from src.requirement import Requirement, Requirement_Concrete
from src.attribute import Attribute
from collections import Counter
import pandas as pd

class SocialBenefit:

    '''
    The class SocialBenefit represents a social benefit and its requirements.

    '''

    def __init__(self, name: str, requirement: Requirement):
        self.name = name
        self.requirement = requirement

    
    def remove_requirement(self) -> None:
        '''
        Removes the requirement from the social benefit.

        '''
        self.requirement = []
        self.set_relevant_attributes()
        print(f"Requirement successfully removed.")

        
    def remove_requirement_by_attribute(self, attribute: Attribute):
        '''
        Removes a requirement from the social benefit by attribute.

        Parameters:
        - attribute (Attribute): The attribute to remove the requirement by.

        '''

        if isinstance(self.requirement, Requirement_Concrete):
            if self.requirement.attribute == attribute:
                self.remove_requirement(self.requirement)
        else: self.requirement.remove_requirement_by_attribute(attribute)
    

    def export(self) -> dict:

        '''
        Exports the social benefit details as a dictionary.

        Returns:
        A dictionary representing the social benefit with its name and requirements.

        '''
        return {
            'name': self.name,
            'requirements': self.requirement.export()
        }
    
    def get_dataframe(self)-> pd.DataFrame:
        '''
        Returns the social benefit requirements as a dataframe.

        Returns:
        DataFrame: A dataframe representing the social benefit requirements.

        '''
        dataframe = self.requirement.get_dataframe()
        dataframe['social_benefit'] = self.name

        return dataframe
