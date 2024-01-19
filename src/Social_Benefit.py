from typing import List, Set
from src.Requirement import Requirement

class Social_Benefit:

    def __init__(self, name: str, requirement: List[Requirement]):
        self.is_relevant = True
        self.name = name
        self.requirement = requirement
        self.relevant_attributes = self.requirement.get_relevant_attributes()

    
    def get_relevant_attributes(self) -> Set[str]:
        return self.relevant_attributes
    
    def reset_evaluations(self):
        self.is_relevant = True
        self.requirement.reset_evaluations()

    def evaluate(self,data) -> bool:
        if any(key in self.relevant_attributes for key in data.keys()):
            result = self.requirement.evaluate(data)
            self.relevant_attributes = self.requirement.get_relevant_attributes()
            if not result:
                self.is_relevant = False
            return result
        else:
            return True
    

    def export(self) -> dict:
        return {
            'name': self.name,
            'requirements': self.requirement.export()
        }
