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

        json_path = "./data/default_data.json"

        default_data = json.load(open(json_path, 'r'))
        self.algorithm.load_data_from_json(json=default_data)

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
    
    def get_user_input_menu_navigation(self,message: str, choices):
        questions = [
            inquirer.List('choice',
                        message=message,
                        choices=choices,
                    ),
        ]
        chosen_function = inquirer.prompt(questions,theme=inquirer.themes.GreenPassion())['choice']
        return chosen_function

    def print_tree(self,requirement, list,level=0, prefix="    "):
        if requirement is not None:
            # print("    " * level + prefix + requirement.get_tree_string())
            list.append("    " * level + prefix + requirement.get_tree_string())
            if isinstance(requirement,Logical_Requirement):
                for i, child in enumerate(requirement.requirements):
                    is_last_child = i == len(requirement.requirements) - 1
                    child_prefix = "└── " if is_last_child else "├── "
                    self.print_tree(requirement=child,list=list, level=level + 1, prefix=child_prefix)

    # Menus
                    
    # Main Menu

    def open_main_menu(self):

        message = "Main Menu"

        choices = [
            ("Start Dialogue", self.start_dialogue),
            ("Edit Attributes", self.show_attributes_in_navigation),
            ("Edit Social Benefits", self.show_social_benefits_in_navigation),
            ("Export Requirements", self.algorithm.export_data_to_json),
            ("Exit", exit)
        ]

        chosen_answer = self.get_user_input_menu_navigation(message=message,choices=choices)

        chosen_answer()

    # Menu for selection of social benefits
        
    def show_social_benefits_in_navigation(self):

        message="Social Benefits"

        choices = [(social_benefit.name, social_benefit) for social_benefit in self.algorithm.social_benefits]
        choices += [("Add Social Benefit", self.open_main_menu)]
        choices += [("<Back>", self.open_main_menu)]

        chosen_answer = self.get_user_input_menu_navigation(message,choices)

        if isinstance(chosen_answer,Social_Benefit):
            chosen_answer()
        else:
            chosen_answer()

    # Menu for editing social benefits
            
    def edit_social_benefit(self,social_benefit:Social_Benefit):
                
            message=f"Edit social benefit '{social_benefit.name}'"
    
            choices=[
                (f"Edit name: '{social_benefit.name}'", self.edit_social_benefit_name),
                (f"Edit requirement-tree", self.edit_social_benefit_requirement),
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
        social_benefit.print_tree()
        self.edit_social_benefit(social_benefit)

    # Menu for selection of attributes
        
    def show_attributes_in_navigation(self):

        message = "Attributes"

        choices = [(attribute.title, attribute) for attribute in self.algorithm.attributes]

        choices += [("<Add Attribute>", self.add_attribute)]

        choices += [("<Back>", self.open_main_menu)]

        chosen_answer = self.get_user_input_menu_navigation(message,choices)

        if isinstance(chosen_answer,Attribute):
            chosen_answer()
        else:
            chosen_answer()

    # Menu for editing attributes
            
    def edit_attribute(self,attribute:Attribute):
            
        message=f"Edit attribute '{attribute.title}'"

        choices=[
            (f"Edit title: '{attribute.title}'", self.edit_attribute_title),
            (f"Edit question: '{attribute.question}'", self.edit_attribute_question),
            (f"Edit possible answers: '{attribute.answer_options}'", self.edit_attribute_answer_options),
            ("<Back>", "back")
        ]

        # Remove answer-options if attribute is numerical
        if isinstance(attribute,Attribute_Categorical):
            choices.pop(2)

        chosen_answer = self.get_user_input_menu_navigation(message,choices)

        if chosen_answer == "back":
            self.show_attributes_in_navigation()
        else:
            chosen_answer(attribute)

    # Menu for editing attribute-title
            
    def edit_attribute_title(self,attribute:Attribute):
        new_title = self.get_user_input_text(question=f"Enter a new title for the attribute '{self.title}'")
        attribute.title = new_title

        self.edit_attribute(attribute)

    # Menu for editing attribute-question
        
    def edit_attribute_question(self,attribute:Attribute):
        new_question = self.get_user_input_text(question=f"Enter a new question for the attribute '{self.title}'")
        attribute.question = new_question

        self.edit_attribute(attribute)

    # Menu for editing attribute-answer-options
        
    def edit_attribute_answer_options(self,attribute:Attribute):
        if isinstance(attribute,Attribute_Categorical):
            new_answer_options = self.get_user_input_text(question=f"Enter new answer options for the attribute, separated by a comma (,) '{self.title}'").split(',')
            attribute.answer_options = new_answer_options

        self.edit_attribute(attribute)


    # Start of the dialogue
        
    def start_dialogue(self):

        while self.algorithm.relevant_attributes:

            best_attribute = self.algorithm.get_best_attribute()

            if isinstance(best_attribute,Attribute_Categorical):
                answer = self.get_user_input_categorical(question_count=self.algorithm.question_count,question=best_attribute.question,choices=best_attribute.answer_options)
            else:
                answer = self.get_user_input_numerical(question_count=self.algorithm.question_count,question=best_attribute.question)

            result = self.algorithm.evaluate({best_attribute.title:answer})


            self.algorithm.question_count += 1

        print(f"Finished questionare. Result: {result}")

        time.sleep(1)

        self.algorithm.reset_evaluation()
        self.open_main_menu()