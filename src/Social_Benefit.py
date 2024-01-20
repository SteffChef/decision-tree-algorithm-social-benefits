from typing import List, Set
from src.Requirement import Requirement

class Social_Benefit:

    def __init__(self, name: str, requirement: List[Requirement]):
        self.is_relevant = True
        self.name = name
        self.requirement = requirement
        self.relevant_attributes = self.requirement.get_relevant_attributes()
    
    def remove_requirement(self):
        self.requirement = []
        self.set_relevant_attributes()
        print(f"Requirement successfully removed.")

    
    def get_relevant_attributes(self) -> Set[str]:
        return self.relevant_attributes
    
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
                self.relevant_attributes = set()
            if not result or len(self.relevant_attributes) == 0:
                self.is_relevant = False           
            return result
        else:
            return True
    

    def export(self) -> dict:
        return {
            'name': self.name,
            'requirements': self.requirement.export()
        }
