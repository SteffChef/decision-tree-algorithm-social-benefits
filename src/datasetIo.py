import json
from src.attribute import Attribute_Numerical, Attribute_Categorical,Attribute
from src.socialBenefit import SocialBenefit
from src.requirement import Logical_AND, Logical_OR, Requirement_Categorical, Requirement_Numerical, Requirement
from typing import List, Tuple, Dict

    
def load_data_from_json(file_path: str) -> Tuple[List[Attribute], List[SocialBenefit]]:
    """
    Loads attributes and social benefits data from a JSON file.

    Parameters:
    - file_path (str): The path to the JSON file to load the data from.

    Returns:
    Tuple[List[Attribute], List[SocialBenefit]]: A tuple containing a list of Attribute objects and a list of SocialBenefit objects. 
    """

    # Try to load the data from the JSON file; if it fails, load the default data
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
    
    except FileNotFoundError:
        print("No exported data found. Loading default data.")
        with open("./data/default_data.json", 'r', encoding='utf-8') as file:
            json_data = json.load(file)

    attribute_list = load_attributes_from_json(json_data['attributes'])
    social_benefit_list = load_social_benefits_from_json(json_data['social_benefits'], attribute_list)

    return attribute_list, social_benefit_list

def load_social_benefits_from_json(json_data: List[Dict], attribute_list: List[Attribute]) -> List[SocialBenefit]:

    """
    Loads social benefits from a JSON structure, using the provided attributes for reference.

    Parameters:
    - json_data (List[Dict]): The JSON data for the social benefits.
    - attribute_list (List[Attribute]): A list of attributes to reference when creating requirements.

    Returns:
    List[SocialBenefit]: A list of SocialBenefit objects.
    """

    def from_json(json_data: Dict) -> 'Requirement':
        # Factory method to instantiate the correct type based on the 'type' field in JSON
        type_mapping = {
            'AND': logical_and_from_json,
            'OR': logical_or_from_json,
            'attribute_categorical': requirement_categorical_from_json,
            'attribute_numerical': requirement_numerical_from_json
        }

        if json_data['type'] not in type_mapping:
            raise ValueError(f"Unknown type: {json_data['type']}")
        
        requirement = type_mapping[json_data['type']](json_data['content'])

        return requirement
    

    # Constructor function for categorical requirements
    def requirement_categorical_from_json(json_data: Dict) -> 'Requirement_Categorical':
        return Requirement_Categorical(attribute=get_attribute_from_title(json_data['title'],attribute_list), required_value=json_data['required_value'])

    # Constructor function for numerical requirements
    def requirement_numerical_from_json(json_data: Dict) -> 'Requirement_Numerical':
        return Requirement_Numerical(attribute=get_attribute_from_title(json_data['title'], attribute_list), comparison_operator=json_data['comparison_operator'], required_value=json_data['required_value'])

    # Constructor function for logical OR requirements
    def logical_or_from_json(json_data: Dict) -> 'Logical_OR':
        requirement = Logical_OR([from_json(v) for v in json_data])
        for req in requirement.requirements:
            req.parent = requirement 
        return requirement

    # Constructor function for logical AND requirements
    def logical_and_from_json(json_data: Dict) -> 'Logical_AND':
        requirement = Logical_AND([from_json(v) for v in json_data])
        for req in requirement.requirements:
            req.parent = requirement    
        return requirement
    
    # Helper function to get an attribute from the attribute list based on its title
    def get_attribute_from_title(title: str,attribute_list) -> Attribute:
        for attribute in attribute_list:
            if attribute.title == title:
                return attribute
        return None

    return [SocialBenefit(v['name'], from_json(v['requirements'])) for v in json_data]

def load_attributes_from_json(json_data: List[Dict]) -> List[Attribute]:
    """
    Loads attributes from a JSON structure.

    Parameters:
    - json_data (List[Dict]): The JSON data for the attributes.

    Returns:
    List[Attribute]: A list of Attribute objects.
    """

    # Define a factory method to instantiate the correct attribute type based on the 'type' field in the JSON
    def from_json(attribute_json: Dict):
        # Mapping of attribute types to their respective construction functions
        type_mapping = {
            'attribute_categorical': attribute_categorical_from_json,
            'attribute_numerical': attribute_numerical_from_json
        }

        # Get the constructor function from the mapping based on the attribute type
        constructor = type_mapping.get(attribute_json['type'])

        # If a constructor is found, instantiate the attribute; otherwise, return None
        if constructor:
            return constructor(attribute_json)
        else:
            raise ValueError(f"Unknown attribute type: {attribute_json['type']}")

    # Constructor function for categorical attributes
    def attribute_categorical_from_json(json_data: Dict) -> 'Attribute_Categorical':
        # Instantiate and return an Attribute_Categorical object
        return Attribute_Categorical(json_data['title'], json_data['question'], json_data['answer_options'])
    
    # Constructor function for numerical attributes
    def attribute_numerical_from_json(json_data: Dict) -> 'Attribute_Numerical':
        # Instantiate and return an Attribute_Numerical object
        return Attribute_Numerical(json_data['title'], json_data['question'], json_data['min'], json_data['max'])

    # Use list comprehension with the factory method to instantiate attributes based on their type
    return [from_json(attribute) for attribute in json_data]


def export_data_to_json(attribute_list:List[Attribute], social_benefits_list:List[SocialBenefit]) -> None:
    """
    Exports the provided attributes and social benefits to a JSON file.

    Parameters:
    - attribute_list (List[Attribute]): A list of attributes to export.
    - social_benefits_list (List[SocialBenefit]): A list of social benefits to export.
    """
    data = {
        'attributes': [
            attribute.export() for attribute in attribute_list
        ],
        'social_benefits': [
            social_benefit.export() for social_benefit in social_benefits_list
        ]
    }

    file_path = './data/exported_data/exported_data.json'

    with open(file_path, 'w',encoding='utf-8') as json_file:
        json.dump(data, json_file,ensure_ascii=False,indent=4)

    print(f"Data has been written to {file_path} as a JSON file.")
