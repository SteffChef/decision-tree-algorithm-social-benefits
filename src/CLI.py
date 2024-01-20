import inquirer
from typing import List,Set
from src.Algorithm import Algorithm
from src.Attribute import Attribute, Attribute_Categorical, Attribute_Numerical
from src.Requirement import Logical_Requirement, Logical_AND, Logical_OR, Requirement_Categorical, Requirement_Numerical
from src.Social_Benefit import Social_Benefit
import json
import time


class CLI:

    def __init__(self,algorithm:Algorithm):
        self.algorithm = algorithm

    def run(self):

        # load exported data from json
        # if there is no exported data, load default data from json
        try:
            print("Loading exported data.")
            json_path = "./data/exported_data/exported_data.json"
            data = json.load(open(json_path, 'r'))
        except:
            print("No exported data found. Loading default data.")
            json_path = "./data/default_data.json"
            data = json.load(open(json_path, 'r'))

        self.algorithm.load_data_from_json(json=data)

        self.open_main_menu()

    # Basic User Input

    def get_user_input_categorical(self,question_count:int,question: str, choices: List[str]) -> str:
        questions = [
            inquirer.List('choice',
                        message=f"Question {question_count}: {question}",
                        choices=choices,
                    ),
        ]
        answers = inquirer.prompt(questions,theme=inquirer.themes.GreenPassion())
        return answers['choice']

    def get_user_input_numerical(self,question_count:int,question: str) -> int:
        questions = [
            inquirer.Text('choice',
                        message=f"Question {question_count}: {question}",
                    ),
        ]
        answers = inquirer.prompt(questions,theme=inquirer.themes.GreenPassion())

        return int(answers['choice'])
    
    def get_user_input_text(self,question:str) -> str:
        questions = [
            inquirer.Text('choice',
                        message=question,
                    ),
        ]
        answers = inquirer.prompt(questions,theme=inquirer.themes.GreenPassion())
        return answers['choice']
    
    def get_user_input_confirm(self,question:str) -> bool:
        questions = [
            inquirer.Confirm('choice',
                        message=question,
                    ),
        ]
        answers = inquirer.prompt(questions,theme=inquirer.themes.GreenPassion())
        return answers['choice']
    
    def get_user_input_menu_navigation(self,message: str, choices):
        questions = [
            inquirer.List('choice',
                        message=message,
                        choices=choices,
                    ),
        ]
        chosen_function = inquirer.prompt(questions,theme=inquirer.themes.GreenPassion())['choice']


        return chosen_function

    def calculate_requirement_tree(self,requirement, list,level=0, prefix="    "):
        if requirement is not None:
            # print("    " * level + prefix + requirement.get_tree_string())
            list.append(("    " * level + prefix + requirement.get_tree_string(),requirement))
            if isinstance(requirement,Logical_Requirement):
                for i, child in enumerate(requirement.requirements):
                    is_last_child = i == len(requirement.requirements) - 1
                    child_prefix = "└── " if is_last_child else "├── "
                    self.calculate_requirement_tree(requirement=child,list=list, level=level + 1, prefix=child_prefix)

    # Menus
                    
    # Main Menu

    def open_main_menu(self):

        message = "Main Menu"

        choices = [
            ("Start Dialogue", self.start_dialogue),
            ("Edit Attributes", self.show_attributes_in_navigation),
            ("Edit Social Benefits", self.show_social_benefits_in_navigation),
            ("Export Data", self.algorithm.export_data_to_json),
            ("<Exit>", exit)
        ]

        chosen_answer = self.get_user_input_menu_navigation(message=message,choices=choices)

        chosen_answer()

    # Menu for selection of social benefits
        
    def show_social_benefits_in_navigation(self):

        message="Social Benefits"

        choices = [(social_benefit.name, social_benefit) for social_benefit in self.algorithm.social_benefits]
        choices += [("<Add Social Benefit>", self.open_main_menu)]
        choices += [("<Back>", self.open_main_menu)]

        chosen_answer = self.get_user_input_menu_navigation(message,choices)

        if isinstance(chosen_answer,Social_Benefit):
            self.edit_social_benefit(social_benefit=chosen_answer)
        else:
            chosen_answer()

    # Menu for editing social benefits
            
    def edit_social_benefit(self,social_benefit:Social_Benefit):
                
            message=f"Edit social benefit '{social_benefit.name}'"
    
            choices=[
                (f"Edit name: '{social_benefit.name}'", self.edit_social_benefit_name),
                ("Edit requirement-tree", self.edit_social_benefit_requirement),
                ("<Back>", "back")
            ]
    
            chosen_answer = self.get_user_input_menu_navigation(message,choices)
    
            if chosen_answer == "back":
                self.show_social_benefits_in_navigation()
            else:
                chosen_answer(social_benefit)

    # Menu for editing social benefit-name
                
    def edit_social_benefit_name(self,social_benefit:Social_Benefit):

        new_name = self.get_user_input_text(question=f"Enter a new name for the social benefit '{social_benefit.name}'")
        social_benefit.name = new_name

        self.edit_social_benefit(social_benefit)

    # Menu for editing social benefit-requirement-tree
        
    def edit_social_benefit_requirement(self,social_benefit:Social_Benefit):

        message = f"Edit requirement-tree for social benefit '{social_benefit.name}'"

        choices = []
        self.calculate_requirement_tree(requirement=social_benefit.requirement,list=choices)

        choices += [
            ("<Back>", self.edit_social_benefit)
        ]

        chosen_answer = self.get_user_input_menu_navigation(message,choices)
        
        if isinstance(chosen_answer,Logical_Requirement):
            self.edit_logical_requirement(logical_requirement=chosen_answer,social_benefit=social_benefit)
        elif isinstance(chosen_answer,Requirement_Categorical):
            self.edit_requirement_categorical(chosen_answer)
        elif isinstance(chosen_answer,Requirement_Numerical):
            self.edit_requirement_numerical(chosen_answer)
        else:
            self.edit_social_benefit(social_benefit)

    # Menu for editing logical requirements
    
    def edit_logical_requirement(self,logical_requirement:Logical_Requirement,social_benefit:Social_Benefit):
            
            message = f"Edit logical requirement '{logical_requirement.get_tree_string()}'"

            # to be finished

                

            choices = [
                ("Add AND", "back"),
                ("Add OR", "back"),
                ("Add Concrete Requirement", "back"),
                ("<Back>", "back")
            ]

            if logical_requirement.parent is not None:
                choices.insert(0,("Remove Requirement", logical_requirement.parent.remove_requirement))
            else:
                choices.insert(0,("Remove Requirement", social_benefit.remove_requirement))
    
            chosen_answer = self.get_user_input_menu_navigation(message,choices)
    
            if chosen_answer == "back":
                self.edit_social_benefit_requirement(social_benefit=social_benefit)
            else:
                confirmation = self.get_user_input_confirm("Are you sure you want to remove this requirement?")
                if confirmation:
                    chosen_answer(logical_requirement)
                    self.edit_social_benefit_requirement(social_benefit=social_benefit)
                else:
                    self.edit_logical_requirement(logical_requirement,social_benefit)

    # Menu for selection of attributes
        
    def show_attributes_in_navigation(self):

        message = "Attributes"

        choices = [(attribute.title, attribute) for attribute in self.algorithm.attributes]

        choices += [("<Add Attribute>", exit)]

        choices += [("<Back>", self.open_main_menu)]

        chosen_answer = self.get_user_input_menu_navigation(message,choices)

        if isinstance(chosen_answer,Attribute):
            self.edit_attribute(attribute=chosen_answer)
        else:
            chosen_answer()

    # Menu for editing attributes
            
    def edit_attribute(self,attribute:Attribute):
            
        message=f"Edit attribute '{attribute.title}'"

        choices=[
            (f"Edit title: '{attribute.title}'", self.edit_attribute_title),
            (f"Edit question: '{attribute.question}'", self.edit_attribute_question),
            ("<Back>", "back")
        ]

        # Insert answer-options if attribute is numerical
        if isinstance(attribute,Attribute_Categorical):
            choices.insert(2,(f"Edit possible answers: '{attribute.answer_options}'", self.edit_attribute_answer_options))

        chosen_answer = self.get_user_input_menu_navigation(message,choices)

        if chosen_answer == "back":
            self.show_attributes_in_navigation()
        else:
            chosen_answer(attribute)

    # Menu for editing attribute-title
            
    def edit_attribute_title(self,attribute:Attribute):
        new_title = self.get_user_input_text(question=f"Enter a new title for the attribute '{attribute.title}'")
        attribute.title = new_title

        self.edit_attribute(attribute)

    # Menu for editing attribute-question
        
    def edit_attribute_question(self,attribute:Attribute):
        new_question = self.get_user_input_text(question=f"Enter a new question for the attribute '{attribute.question}'")
        attribute.question = new_question

        self.edit_attribute(attribute)

    # Menu for editing attribute-answer-options
        
    def edit_attribute_answer_options(self,attribute:Attribute):
        if isinstance(attribute,Attribute_Categorical):
            new_answer_options = self.get_user_input_text(question=f"Enter new answer options for the attribute, separated by a comma (,) '{attribute.title}'").split(',')
            attribute.answer_options = new_answer_options

        self.edit_attribute(attribute)


    # Start of the dialogue
        
    def start_dialogue(self):

        while self.algorithm.relevant_attributes:

            print(f"Relevant Attributes: {self.algorithm.relevant_attributes}")

            best_attribute = self.algorithm.get_best_attribute()

            if isinstance(best_attribute,Attribute_Categorical):
                answer = self.get_user_input_categorical(question_count=self.algorithm.question_count,question=best_attribute.question,choices=best_attribute.answer_options)
            else:
                answer = self.get_user_input_numerical(question_count=self.algorithm.question_count,question=best_attribute.question)

            result = self.algorithm.evaluate({best_attribute.title:answer})


            self.algorithm.question_count += 1

        print(f"Finished questionnaire. Result: {result}")

        time.sleep(1)

        self.algorithm.reset_evaluation()
        self.open_main_menu()