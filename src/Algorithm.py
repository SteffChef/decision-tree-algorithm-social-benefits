from src.Requirement import Logical_AND, Logical_OR, Requirement_Categorical, Requirement_Numerical
from src.Social_Benefit import Social_Benefit
from src.Attribute import Attribute, Attribute_Categorical, Attribute_Numerical
from typing import List,Set
import json

class Algorithm:

    def __init__(self):
        self.question_count = 1

    def load_requirements_from_json(self,json: dict):

        def requirement_categorical_from_json(json: dict,parent = None) -> 'Requirement_Categorical':

            req =  Requirement_Categorical(attribute=self.get_attribute_from_title(json['title']), required_value=json['required_value'])

            if parent is not None:
                req.parent = parent
            
            return req
        
        def requirement_numerical_from_json(json: dict, parent = None) -> 'Requirement_Numerical':
            req =  Requirement_Numerical(attribute=self.get_attribute_from_title(json['title']),vergleichsoperator=json['vergleichsoperator'], required_value=json['required_value'] )

            if parent is not None:
                req.parent = parent
            
            return req
        
        def logical_or_from_json(json: dict,parent = None) -> 'Logical_OR':
            requirements = [logical_and_from_json(v) if v['type'] == 'AND'
                            else logical_or_from_json(v) if v['type'] == 'OR'
                            else requirement_categorical_from_json(v['content']) if v['type'] == 'attribute_categorical'
                            else requirement_numerical_from_json(v['content']) if v['type'] == 'attribute_numerical'
                            else None for v in json['content']]

            req = Logical_OR(requirements)

            if parent is not None:
                req.parent = parent

            for requirement in req.requirements:
                requirement.parent = req
            
            return req
        
        def logical_and_from_json(json: dict,parent = None) -> 'Logical_AND':
            requirements = [logical_and_from_json(v) if v['type'] == 'AND'
                            else logical_or_from_json(v) if v['type'] == 'OR'
                            else requirement_categorical_from_json(v['content']) if v['type'] == 'attribute_categorical'
                            else requirement_numerical_from_json(v['content']) if v['type'] == 'attribute_numerical'
                            else None for v in json['content']]

            req = Logical_AND(requirements)

            if parent is not None:
                req.parent = parent
            
            for requirement in req.requirements:
                requirement.parent = req
            
            return req
        
        def social_benefit_from_json(json: dict) -> 'Social_Benefit':
            if json['requirements']['type'] == 'AND':
                requirement = logical_and_from_json(json['requirements'])
            elif json['requirements']['type'] == 'OR':
                requirement = logical_or_from_json(json['requirements'])
            elif json['requirements']['type'] == 'attribute_categorical':
                requirement = requirement_categorical_from_json(json['requirements']['content'])
            elif json['requirements']['type'] == 'attribute_numerical':
                requirement = requirement_numerical_from_json(json['requirements']['content'])
            else:
                raise ValueError(f'Unknown type')

            return Social_Benefit(json['name'], requirement)
        
        self.social_benefits = [social_benefit_from_json(v) for v in json]

        self.set_relevant_attributes()
        self.evaluation = {social_benefit.name:True for social_benefit in self.social_benefits}

    def load_attributes_from_json(self,json: dict):

        def attribute_categorical_from_json(json: dict) -> 'Attribute_Categorical':
            return Attribute_Categorical(json['title'], json['question'] , json['answer_options'])
        
        def attribute_numerical_from_json(json: dict) -> 'Attribute_Numerical':
            return Attribute_Numerical(json['title'],json['question'])
        
        self.attributes = [attribute_categorical_from_json(attribute) if attribute['type'] == 'attribute_categorical'
                           else attribute_numerical_from_json(attribute) if attribute['type'] == 'attribute_numerical'
                           else None for attribute in json]
        
    def load_data_from_json(self,json:dict):
        self.load_attributes_from_json(json['attributes'])
        self.load_requirements_from_json(json['social_benefits'])

    def export_data_to_json(self) -> dict:
        data = {
            'attributes': [
                attribute.export() for attribute in self.attributes
            ],
            'social_benefits': [
                social_benefit.export() for social_benefit in self.social_benefits
            ]
        }

        file_path = './data/exported_data/exported_data.json'

        with open(file_path, 'w',encoding='utf-8') as json_file:
            json.dump(data, json_file,ensure_ascii=False,indent=4)

        print(f"Data have been written to {file_path} as a JSON file.")
        
    
    def export_requirements_to_json(self) -> dict:
        data = {
            'social_benefits': [
                social_benefit.export() for social_benefit in self.social_benefits
            ]
        }

        file_path = 'exported_requirements.json'

        with open(file_path, 'w',encoding='utf-8') as json_file:
            json.dump(data, json_file,ensure_ascii=False,indent=4)

        print(f"Social Benefits have been written to {file_path} as a JSON file.")

    def export_attributes_to_json(self) -> dict:
        data = [
            {
                'type': 'attribute_categorical',
                'title': attribute.title,
                'question': attribute.question,
                'answer_options': attribute.answer_options
            } if isinstance(attribute,Attribute_Categorical)
            else {
                'type': 'attribute_numerical',
                'title': attribute.title,
                'question': attribute.question
            } if isinstance(attribute,Attribute_Numerical)
            else None for attribute in self.attributes
        ]

        file_path = 'exported_attributes.json'

        with open(file_path, 'w',encoding='utf-8') as json_file:
            json.dump(data, json_file,ensure_ascii=False,indent=4)

        print(f"Attributes have been written to {file_path} as a JSON file.")

    
    def set_relevant_attributes(self) -> Set[str]:
        data = {}
        for social_benefit in self.social_benefits:
            if social_benefit.is_relevant:
                for element in social_benefit.get_relevant_attributes():
                    if element in data.keys():
                        data[element] += 1
                    else:
                        data[element] = 1
        self.relevant_attributes = data

    def get_relevant_social_benefits(self) -> Set[str]:
        return self.relevant_attributes
    
    def evaluate(self,data):
        for social_benefit in self.social_benefits:
            if social_benefit.is_relevant:
                self.evaluation[social_benefit.name] = social_benefit.evaluate(data)
        self.set_relevant_attributes()
        return self.evaluation
    
    def get_attribute_from_title(self,title: str) -> Attribute:
        for attribute in self.attributes:
            if attribute.title == title:
                return attribute
        return None

    # Attributsauswahl! Verbessern
    def get_best_attribute(self) -> Attribute:
        best_attribute_title = max(self.relevant_attributes, key=self.relevant_attributes.get)
        return self.get_attribute_from_title(best_attribute_title)
    
    def reset_evaluation(self):
        for social_benefit in self.social_benefits:
            social_benefit.reset_evaluations()
        self.set_relevant_attributes()
        self.question_count = 1