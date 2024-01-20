from typing import List, Set
from src.Attribute import Attribute

class Requirement:

    def __init__(self):
        self.is_relevant = True
        self.parent = None
    
    def set_parent(self, parent: 'Requirement'):
        self.parent = parent

class Logical_Requirement(Requirement):

    def __init__(self, requirements: List[Requirement]):
        super().__init__()
        self.requirements = requirements
        self.set_relevant_attributes()

    def set_relevant_attributes(self) -> Set[str]:
        data = set()
        for requirement in self.requirements:
            if requirement.is_relevant:
                data.update(requirement.get_relevant_attributes())
        if len(data) == 0:
            self.is_relevant = False
        self.relevant_attributes = data

    def get_relevant_attributes(self) -> Set[str]:
        return self.relevant_attributes
    
    def reset_evaluations(self):
        self.is_relevant = True
        for requirement in self.requirements:
            requirement.reset_evaluations()

    def remove_requirement(self, requirement: Requirement):
        self.requirements.remove(requirement)
        self.set_relevant_attributes()
        if self.parent is not None:
            self.parent.set_relevant_attributes()
        print(f"Requirement {requirement.get_tree_string()} successfully removed.")

class Logical_AND(Logical_Requirement):

    def evaluate(self, data: dict) -> bool:
        if any(key in self.relevant_attributes for key in data.keys()):
            for requirement in self.requirements:
                if not requirement.evaluate(data):
                    self.is_relevant = False
                    return False
        self.set_relevant_attributes()
        return True
        
    def get_tree_string(self) -> str:
        return 'AND'
    
    def export(self) -> dict:
        return {
            'type': 'AND',
            'content': [requirement.export() for requirement in self.requirements]
        }

class Logical_OR(Logical_Requirement):
    
    # should one requirement be true, the whole requirement is true, otherwise false
    def evaluate(self, data: dict) -> bool:
        if any(key in self.relevant_attributes for key in data.keys()):
            for requirement in self.requirements:
                if requirement.evaluate(data):
                    self.is_relevant = False
                    return True
            return False
        else:
            return True
        
    def get_tree_string(self) -> str:
        return 'OR'
    
    def export(self) -> dict:
        return {
            'type': 'OR',
            'content': [requirement.export() for requirement in self.requirements]
        }
    
class Requirement_Concrete(Requirement):

    def __init__(self, attribute: Attribute):
        super().__init__()
        self.attribute = attribute

    
    def get_relevant_attributes(self) -> Set[str]:
        return {self.attribute.title}
    
    def reset_evaluations(self):
        self.is_relevant = True


class Requirement_Numerical(Requirement_Concrete):

    def __init__(self,  attribute: Attribute, vergleichsoperator: str, required_value: List[int]):
        super().__init__(attribute=attribute)
        self.vergleichsoperator = vergleichsoperator
        self.required_value = required_value


    def evaluate(self,data) -> bool:
        if any(key == self.attribute.title for key in data.keys()):
            self.is_relevant = False
            value = data[self.attribute.title]
            if self.vergleichsoperator == '<':
                return value < self.required_value[0]
            if self.vergleichsoperator == '<=':
                return value <= self.required_value[0]
            if self.vergleichsoperator == '>':
                return value > self.required_value[0]
            if self.vergleichsoperator == '>=':
                return value >= self.required_value[0]
            if self.vergleichsoperator == '==':
                return value == self.required_value[0]
            if self.vergleichsoperator == '[]':
                return value >= self.required_value[0] and value <= self.required_value[1]
            return True
        else:
            return True
        
    def get_tree_string(self) -> str:
        return f'{self.attribute.title} {self.vergleichsoperator} {self.required_value}'
    
    def export(self) -> dict:
        return {
            'type': 'attribute_numerical',
            'content': {
                'title': self.attribute.title,
                'vergleichsoperator': self.vergleichsoperator,
                'required_value': self.required_value
            }
        }

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
    
    def export(self) -> dict:
        return {
            'type': 'attribute_categorical',
            'content': {
                'title': self.attribute.title,
                'required_value': self.required_value
            }
        }