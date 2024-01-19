from typing import List,Set
import json
import inquirer
import inspect
import time

class UserInterface:
    
    @staticmethod
    def get_user_input_categorical(question_count:int,question: str, choices: List[str]) -> str:
        questions = [
            inquirer.List('choice',
                        message=f"Question {question_count}: {question}",
                        choices=choices,
                    ),
        ]
        answers = inquirer.prompt(questions,theme=inquirer.themes.GreenPassion())
        return answers['choice']
    
    @staticmethod
    def get_user_input_numerical(question_count:int,question: str) -> int:
        questions = [
            inquirer.Text('choice',
                        message=f"Question {question_count}: {question}",
                    ),
        ]
        answers = inquirer.prompt(questions,theme=inquirer.themes.GreenPassion())

        return int(answers['choice'])
    
    @staticmethod
    def get_user_input_text(question:str) -> str:
        questions = [
            inquirer.Text('choice',
                        message=question,
                    ),
        ]
        answers = inquirer.prompt(questions,theme=inquirer.themes.GreenPassion())
        return answers['choice']
    
    @staticmethod
    def get_user_input_menu_navigation(question: str, choices,returnfunction:callable):
        questions = [
            inquirer.List('choice',
                        message=question,
                        choices=choices,
                    ),
        ]
        choosen_function = inquirer.prompt(questions,theme=inquirer.themes.GreenPassion())['choice']
        params = inspect.signature(choosen_function).parameters
        if params:
            choosen_function(returnfunction)
        else:
            choosen_function()
    
    @staticmethod
    def print_tree(requirement, list,level=0, prefix="    "):
        if requirement is not None:
            # print("    " * level + prefix + requirement.get_tree_string())
            list.append("    " * level + prefix + requirement.get_tree_string())
            if isinstance(requirement,Logical_Requirement):
                for i, child in enumerate(requirement.requirements):
                    is_last_child = i == len(requirement.requirements) - 1
                    child_prefix = "└── " if is_last_child else "├── "
                    UserInterface.print_tree(requirement=child,list=list, level=level + 1, prefix=child_prefix)

class Attribute:
    
    def __init__(self, title: str, question:str):
        self.title = title
        self.question = question

    def edit_title(self,returnfunction: callable):
        self.title = UserInterface.get_user_input_text(question=f"Enter a new title for the attribute '{self.title}'")
        self.edit(returnfunction=returnfunction)

    def edit_question(self,returnfunction: callable):
        self.title = UserInterface.get_user_input_text(question=f"Enter a new question for the attribute '{self.title}'")
        self.edit(returnfunction=returnfunction)

        
class Attribute_Categorical(Attribute):
    
    def __init__(self, title: str,question:str, answer_options: List[str]):
        super().__init__(title,question)
        self.answer_options = answer_options
    
    def edit_answer_options(self,returnfunction: callable):
        self.answer_options = UserInterface.get_user_input_text(question="Type in new answer options, seperated by a comma (,)").split(',')
        self.edit(returnfunction=returnfunction)

    def edit(self,returnfunction: callable):

        message=f"Edit attribute '{self.title}'"

        choices=[
            (f"Edit title: '{self.title}'", self.edit_title),
            (f"Edit question: '{self.question}'", self.edit_question),
            (f"Edit possible answers: '{self.answer_options}'", self.edit_answer_options),
            ("<Back>", returnfunction)
        ]

        UserInterface.get_user_input_menu_navigation(message,choices,returnfunction)

    def export(self) -> dict:
        return {
            'type': 'attribute_categorical',
            'title': self.title,
            'question': self.question,
            'answer_options': self.answer_options
        }
        
class Attribute_Numerical(Attribute):
                
    def edit(self,returnfunction: callable):

        message=f"Edit attribute '{self.title}'"

        choices=[
            (f"Edit title: '{self.title}'", self.edit_title),
            (f"Edit question: '{self.question}'", self.edit_question),
            ("<Back>", returnfunction)
        ]

        UserInterface.get_user_input_menu_navigation(message,choices,returnfunction)

    def export(self) -> dict:
        return {
            'type': 'attribute_numerical',
            'title': self.title,
            'question': self.question
        }
            
class Requirement:

    def __init__(self):
        self.is_relevant = True

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
        

    def print_tree(self):
        print(f"Requirement-tree of Social Benefit {self.name}:")

        list = []
        UserInterface.print_tree(requirement=self.requirement,list=list)

        menu_questions = [
            inquirer.List("choice",
                        message="Requirement-tree",
                        choices=list,
                        ),
        ]
        inquirer.prompt(menu_questions, theme=inquirer.themes.GreenPassion())

    def export(self) -> dict:
        return {
            'name': self.name,
            'requirements': self.requirement.export()
        }

class Algorithm:

    def __init__(self):
        self.question_count = 1

    def load_requirements_from_json(self,json: dict):

        def requirement_categorical_from_json(json: dict) -> 'Requirement_Categorical':
            return Requirement_Categorical(attribute=self.get_attribute_from_title(json['title']), required_value=json['required_value'])
        
        def requirement_numerical_from_json(json: dict) -> 'Requirement_Numerical':
            return Requirement_Numerical(attribute=self.get_attribute_from_title(json['title']),vergleichsoperator=json['vergleichsoperator'], required_value=json['required_value'] )
        
        def logical_or_from_json(json: dict) -> 'Logical_OR':
            requirements = [logical_and_from_json(v) if v['type'] == 'AND'
                            else logical_or_from_json(v) if v['type'] == 'OR'
                            else requirement_categorical_from_json(v['content']) if v['type'] == 'attribute_categorical'
                            else requirement_numerical_from_json(v['content']) if v['type'] == 'attribute_numerical'
                            else None for v in json['content']]

            return Logical_OR(requirements)
        
        def logical_and_from_json(json: dict) -> 'Logical_AND':
            requirements = [logical_and_from_json(v) if v['type'] == 'AND'
                            else logical_or_from_json(v) if v['type'] == 'OR'
                            else requirement_categorical_from_json(v['content']) if v['type'] == 'attribute_categorical'
                            else requirement_numerical_from_json(v['content']) if v['type'] == 'attribute_numerical'
                            else None for v in json['content']]

            return Logical_AND(requirements)
        
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
                raise ValueError(f'Unbekannter type')

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
    
    # Menu Navigation
    def open_main_menu(self):

        message="Main Menu"

        choices=[
            ("Start Dialogue", self.start_dialogue),
            ("Edit Social Benefits", self.show_social_benefits_in_navigation),
            ("Edit Attributes", self.show_attributes_in_navigation),
            ("<Exit>", exit)
        ]

        UserInterface.get_user_input_menu_navigation(message,choices,self.open_main_menu)

    # Menu for selection of social benefits
    def show_social_benefits_in_navigation(self):

        choises = [(social_benefit.name, social_benefit.print_tree) for social_benefit in self.social_benefits]

        choises += [("Add Social Benefit", exit)]

        choises += [("Export Requirements", self.export_data_to_json)]
        
        choises += [("<Back>", self.open_main_menu)]

        menu_questions = [
            inquirer.List("choice",
                        message="Social Benefits",
                        choices=choises,
                        ),
        ]


        selected_option = inquirer.prompt(menu_questions, theme=inquirer.themes.GreenPassion())
        selected_option['choice']()

    # Menu for selection of attributes
    def show_attributes_in_navigation(self):

        message = "Edit Attributes"

        choises = [(attribute.title, attribute.edit) for attribute in self.attributes]

        choises += [("<Add Attribute>", exit)]

        choises += [("<Export Attributes>", self.export_data_to_json)]

        choises += [("<Back>", self.open_main_menu)]

        UserInterface.get_user_input_menu_navigation(message,choises,self.show_attributes_in_navigation)
    
    # Start of the dialogue
    def start_dialogue(self):

        while self.relevant_attributes:

            best_attribute = self.get_best_attribute()

            if isinstance(best_attribute,Attribute_Categorical):
                answer = UserInterface.get_user_input_categorical(question_count=self.question_count,question=best_attribute.question,choices=best_attribute.answer_options)
            else:
                answer = UserInterface.get_user_input_numerical(question_count=self.question_count,question=best_attribute.question)

            result = self.evaluate({best_attribute.title:answer})


            self.question_count += 1

        print(f"Finished Questionare. Result: {result}")

        time.sleep(1)

        self.reset_evaluation()
        self.open_main_menu()


if __name__ == '__main__':

    algorithm = Algorithm()

    # Construct the full path to the JSON file
    json_path = "./data/default_data.json"

    default_data = json.load(open(json_path, 'r'))
    algorithm.load_data_from_json(json=default_data)

    algorithm.open_main_menu()

    # algorithm.start_dialogue()