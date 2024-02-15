from typing import List, Set
from requirement import Requirement, Requirement_Concrete
from attribute import Attribute
from collections import Counter
import pandas as pd

class SocialBenefit:

    def __init__(self, name: str, requirement: Requirement):

        self.is_relevant = True
        self.name = name
        self.requirement = requirement

        # not sure if this is the right way to do it
        self.attribute_counts = None
    
    def remove_requirement(self):
        self.requirement = []
        self.set_relevant_attributes()
        print(f"Requirement successfully removed.")

    
    def get_relevant_attribute_counts(self) -> Set[str]:
        return self.requirement.get_relevant_attribute_counts()
    
    def reset_evaluations(self):
        self.is_relevant = True
        self.requirement.reset_evaluations()
        self.relevant_attributes = self.requirement.get_relevant_attributes()

    def evaluate(self,data) -> bool:
        if any(key in self.relevant_attributes for key in data.keys()):
            result = self.requirement.evaluate(data)
            if self.requirement.is_relevant:
                self.relevant_attributes = self.requirement.get_relevant_attributes()
            else:
                self.relevant_attributes = Counter()
            if not result or len(self.relevant_attributes) == 0:
                self.is_relevant = False           
            return result
        else:
            return True
        
    def remove_requirement_by_attribute(self, attribute: Attribute):
        if isinstance(self.requirement, Requirement_Concrete):
            if self.requirement.attribute == attribute:
                self.remove_requirement(self.requirement)
        else: self.requirement.remove_requirement_by_attribute(attribute)
    

    def export(self) -> dict:
        return {
            'name': self.name,
            'requirements': self.requirement.export()
        }
    
    def get_dataframe(self):
        dataframe = self.requirement.get_dataframe()
        dataframe['social_benefit'] = self.name

        return dataframe
