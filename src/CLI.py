import inquirer
from typing import List,Set
from src.Algorithm import Algorithm
from src.Attribute import Attribute, Attribute_Categorical, Attribute_Numerical
from src.Requirement import Requirement,Requirement_Logical, Logical_AND, Logical_OR, Requirement_Categorical, Requirement_Numerical
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
    
    def get_user_input_checkbox(self,question:str,choices:List[str]) -> List[str]:
        questions = [
            inquirer.Checkbox('choice',
                        message=question,
                        choices=choices,
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

    # Menus
                    
    # Main Menu

    def open_main_menu(self):

        message = "🏡 Main Menu"

        choices = [
            ("Start Dialogue", self.start_dialogue),
            ("Edit Attributes", self.show_attributes_in_navigation),
            ("Edit Social Benefits", self.show_social_benefits_in_navigation),
            ("Export Data", self.export_data),
            ("<Exit>", exit)
        ]

        chosen_answer = self.get_user_input_menu_navigation(message=message,choices=choices)

        chosen_answer()

    def export_data(self):
        self.algorithm.export_data_to_json()
        time.sleep(1)
        self.open_main_menu()

    # Menu for selection of social benefits
        
    def show_social_benefits_in_navigation(self):

        message="Social Benefits"

        choices = [(social_benefit.name, (self.edit_social_benefit,(social_benefit,))) for social_benefit in self.algorithm.social_benefits]

        choices = sorted(choices, key=lambda x: x[0])

        choices += [("<Add Social Benefit>", (self.add_social_benefit,()))]
        choices += [("<Back>", (self.open_main_menu,()))]

        chosen_answer = self.get_user_input_menu_navigation(message,choices)

        selected_function, parameters = chosen_answer
        selected_function(*parameters)

    # Menu for adding new social benefits
        
    def add_social_benefit(self):
            
        new_social_benefit = Social_Benefit(name="New_Social_Benefit",requirement=Logical_AND(requirements=[]))
        self.algorithm.add_social_benefit(new_social_benefit)

        print(f"New social benefit '{new_social_benefit.name}' added.")

        self.edit_social_benefit(new_social_benefit)

    # Menu for editing social benefits
            
    def edit_social_benefit(self,social_benefit:Social_Benefit):
                
        message=f"Edit social benefit '{social_benefit.name}'"

        choices=[
            (f"Edit name: '{social_benefit.name}'", (self.edit_social_benefit_name,(social_benefit,))),
            ("Edit requirement-tree", (self.edit_social_benefit_requirement,(social_benefit,))),
            ("Delete this Social Benefit", (self.delete_social_benefit,(social_benefit,))),
            ("<Back>", (self.show_social_benefits_in_navigation,()))
        ]

        chosen_answer = self.get_user_input_menu_navigation(message,choices)

        selected_function,parameters = chosen_answer
        selected_function(*parameters)

    def delete_social_benefit(self,social_benefit:Social_Benefit):
        confirmation = self.get_user_input_confirm("Are you sure you want to remove this social benefit?")
        if confirmation:
            self.algorithm.remove_social_benefit(social_benefit)
            time.sleep(1)
            self.show_social_benefits_in_navigation()
        else:
            print(f"Social benefit '{social_benefit.name}' not removed.")
            self.edit_social_benefit(social_benefit)

    # Menu for editing social benefit-name
                
    def edit_social_benefit_name(self,social_benefit:Social_Benefit):

        new_name = self.get_user_input_text(question=f"Enter a new name for the social benefit '{social_benefit.name}'")
        social_benefit.name = new_name

        self.edit_social_benefit(social_benefit)

    # Menu for editing social benefit-requirement-tree
        
    def edit_social_benefit_requirement(self,social_benefit:Social_Benefit):

        def calculate_requirement_tree(requirement, list,level=0, prefix="    "):
            if requirement is not None:

                # print("    " * level + prefix + requirement.get_tree_string())
                list.append(("    " * level + prefix + requirement.get_tree_string(),(self.edit_requirement,(requirement,social_benefit))))
                if isinstance(requirement,Requirement_Logical):
                    for i, child in enumerate(requirement.requirements):
                        is_last_child = i == len(requirement.requirements) - 1
                        child_prefix = "└── " if is_last_child else "├── "
                        calculate_requirement_tree(requirement=child,list=list, level=level + 1, prefix=child_prefix)

        message = f"Edit requirement-tree for social benefit '{social_benefit.name}'"

        choices = []

        calculate_requirement_tree(requirement=social_benefit.requirement,list=choices)

        choices += [
            ("<Back>", (self.edit_social_benefit,(social_benefit,)))
        ]

        chosen_answer = self.get_user_input_menu_navigation(message,choices)
        
        selected_function,parameters = chosen_answer
        selected_function(*parameters)

    # Logic for menu for editing requirements
        
    def edit_requirement(self,requirement:Requirement,social_benefit:Social_Benefit):

        if isinstance(requirement,Requirement_Logical):
            self.edit_requirement_logical(requirement=requirement,social_benefit=social_benefit)
        elif isinstance(requirement,Requirement_Categorical):
            self.edit_requirement_categorical(requirement=requirement,social_benefit=social_benefit)
        elif isinstance(requirement,Requirement_Numerical):
            self.edit_requirement_numerical(requirement=requirement,social_benefit=social_benefit)
        else:
            self.edit_social_benefit_requirement(social_benefit=social_benefit)

    # Menu for editing logical requirements
    
    def edit_requirement_logical(self,requirement:Requirement_Logical,social_benefit:Social_Benefit):
            
            message = f"Edit logical requirement '{requirement.get_tree_string()}'"

            # to be finished

            choices = [
                ("Remove Requirement", (self.remove_requirement,(requirement,social_benefit))),
                ("Add AND", (self.add_requirement_and,(requirement,social_benefit))),
                ("Add OR", (self.add_requirement_or,(requirement,social_benefit))),
                ("Add Concrete Requirement", (self.add_requirement_concrete,(requirement,social_benefit))),
                ("<Back>", (self.edit_social_benefit_requirement,(social_benefit,)))
            ]
    
            chosen_answer = self.get_user_input_menu_navigation(message,choices)
    
            selected_function,parameters = chosen_answer
            selected_function(*parameters)

    def add_requirement_and(self,requirement:Requirement_Logical,social_benefit:Social_Benefit):
        new_logical_requirement = Logical_AND(requirements=[])

        requirement.add_requirement(new_logical_requirement)

        self.edit_social_benefit_requirement(social_benefit=social_benefit)

    def add_requirement_or(self,requirement:Requirement_Logical,social_benefit:Social_Benefit):
        new_logical_requirement = Logical_OR(requirements=[])

        requirement.add_requirement(new_logical_requirement)

        self.edit_social_benefit_requirement(social_benefit=social_benefit)

    # Menu for editing concrete requirements

    def add_requirement_concrete(self,requirement:Requirement,social_benefit:Social_Benefit):

        def add_requirement_concrete_attribute(requirement:Requirement,social_benefit:Social_Benefit,attribute:Attribute):
            if isinstance(attribute,Attribute_Categorical):
                new_requirement = Requirement_Categorical(attribute=attribute,required_value=[attribute.answer_options[0]])
            else:
                new_requirement = Requirement_Numerical(attribute=attribute,comparison_operator='==',required_value=0)

            requirement.add_requirement(new_requirement)
            new_requirement.parent = requirement

            self.edit_requirement(new_requirement,social_benefit)
        
        message = f"Add concrete requirement to '{requirement.get_tree_string()}'"

        choices = [
            (f"{attribute.title}", (add_requirement_concrete_attribute,(requirement,social_benefit,attribute))) for attribute in self.algorithm.attributes
        ]

        choices = sorted(choices, key=lambda x: x[0])

        choices += [("<Back>", (self.edit_social_benefit_requirement,(social_benefit,)))]

        chosen_answer = self.get_user_input_menu_navigation(message,choices)

        selected_function,parameters = chosen_answer
        selected_function(*parameters)

    # Confirmation for removing requirements

    def remove_requirement(self,requirement:Requirement,social_benefit:Social_Benefit):
        confirmation = self.get_user_input_confirm("Are you sure you want to remove this requirement?")
        if confirmation:
            if requirement.parent is not None:
                requirement.parent.remove_requirement(requirement)
            else:
                social_benefit.remove_requirement(requirement)

        # umbennen
        self.edit_social_benefit_requirement(social_benefit=social_benefit)

    # Menu for editing categorical requirements

    def edit_requirement_categorical(self,requirement:Requirement_Categorical,social_benefit:Social_Benefit):

        message = f"Edit categorical requirement '{requirement.attribute.title}' in {requirement.required_value}'"

        choices = [
            (f"Edit required value(s): '{requirement.required_value}'", (self.edit_requirement_categorical_required_value,(requirement,social_benefit))),
            ("Delete this Requirement", (self.remove_requirement,(requirement,social_benefit))),
            ("<Back>", (self.edit_social_benefit_requirement,(social_benefit,)))
        ]

        chosen_answer = self.get_user_input_menu_navigation(message=message,choices=choices)

        selected_function,parameters = chosen_answer
        selected_function(*parameters)

    def edit_requirement_categorical_required_value(self,requirement:Requirement_Categorical,social_benefit:Social_Benefit):

        message = f"Edit required value(s) for attribute '{requirement.attribute.title}' (select with spacebar, confirm with enter)"

        choices = [f"{answer_options}" for answer_options in requirement.attribute.answer_options]

        chosen_answers = self.get_user_input_checkbox(message,choices)

        requirement.required_value = chosen_answers

        self.edit_requirement_categorical(requirement=requirement,social_benefit=social_benefit)


    # Menu for editing numerical requirements

    def edit_requirement_numerical(self,requirement:Requirement_Numerical,social_benefit:Social_Benefit):

        def edit_comparison_operator(requirement:Requirement_Numerical,social_benefit:Social_Benefit):
            message = f"Edit comparison operator for attribute '{requirement.attribute.title}'"

            choices = [(operator,(requirement.set_comparison_operator,(operator,))) for operator in Requirement_Numerical.comparison_operators]

            chosen_answer = self.get_user_input_menu_navigation(message=message,choices=choices)

            selected_function,parameters = chosen_answer
            selected_function(*parameters)

            self.edit_requirement_numerical(requirement=requirement,social_benefit=social_benefit)

        def edit_requirement_numerical_required_value(requirement:Requirement_Numerical,social_benefit:Social_Benefit):

            if requirement.comparison_operator == '[]':
                new_required_value = self.get_user_input_text(question=f"Enter a new required value for the attribute '{requirement.attribute.title}' (separate min and max with a comma (,))").split(',')
                new_required_value = [int(new_required_value[0]),int(new_required_value[1])]
            else:
                new_required_value = self.get_user_input_text(question=f"Enter a new required value for the attribute '{requirement.attribute.title}'")
                new_required_value = [int(new_required_value)]

            if new_required_value == requirement.required_value:
                print("Required value not changed.")
            else:
                requirement.required_value = new_required_value

            self.edit_requirement_numerical(requirement=requirement,social_benefit=social_benefit)
            
        message = f"Edit numerical requirement '{requirement.attribute.title} {requirement.comparison_operator} {requirement.required_value}'"

        choices = [
            (f"Edit Operator: '{requirement.comparison_operator}'", (edit_comparison_operator,(requirement,social_benefit))),
            (f"Edit required value: '{requirement.required_value}'", (edit_requirement_numerical_required_value,(requirement,social_benefit))),
            ("Delete this Requirement", (self.remove_requirement,(requirement,social_benefit))),
            ("<Back>", (self.edit_social_benefit_requirement,(social_benefit,)))
        ]

        chosen_answer = self.get_user_input_menu_navigation(message=message,choices=choices)

        selected_function,parameters = chosen_answer
        selected_function(*parameters)

    # Menu for selection of attributes
        
    def show_attributes_in_navigation(self):
 
        message = "Attributes"

        choices = [(attribute.title, (self.edit_attribute,(attribute,))) for attribute in self.algorithm.attributes]

        choices = sorted(choices, key=lambda x: x[0])

        choices += [("<Add Attribute>", (self.add_attribute,()))]

        choices += [("<Back>", (self.open_main_menu,()))]

        chosen_answer = self.get_user_input_menu_navigation(message,choices)

        selected_function,parameters = chosen_answer
        selected_function(*parameters)

    # Menu for editing attributes
            
    def edit_attribute(self,attribute:Attribute):
            
        message=f"Edit attribute '{attribute.title}'"

        choices=[
            (f"Edit title: '{attribute.title}'", (self.edit_attribute_title,(attribute,))),
            (f"Edit question: '{attribute.question}'", (self.edit_attribute_question,(attribute,))),
            (f"Delete this Attribute", (self.remove_attribute,(attribute,))),
            ("<Back>", (self.show_attributes_in_navigation,()))
        ]

        # Insert answer-options if attribute is numerical
        if isinstance(attribute,Attribute_Categorical):
            choices.insert(2,(f"Edit possible answers: '{attribute.answer_options}'", (self.edit_attribute_answer_options,(attribute,))))

        chosen_answer = self.get_user_input_menu_navigation(message,choices)

        selected_function,parameters = chosen_answer
        selected_function(*parameters)

    # Menu for editing attribute-title
            
    def edit_attribute_title(self,attribute:Attribute):
        new_title = self.get_user_input_text(question=f"Enter a new title for the attribute '{attribute.title}'")

        if new_title == attribute.title or new_title == "":
            print("Title not changed.")
        elif self.algorithm.check_attribute_title(new_title):
            print("Title already exists.")
        else:
            attribute.title = new_title
            print(f"Title changed to '{attribute.title}'.")

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

    # Menu for adding new attributes
    
    def add_attribute(self):

        def add_attribute_numerical():
            new_attribute = Attribute_Numerical(title="New_Attribute_Numerical",question="New Question")
            self.algorithm.add_attribute(new_attribute)

            print(f"New attribute '{new_attribute.title}' added.")

            self.edit_attribute(new_attribute)
        
        def add_attribute_categorical():
            new_attribute = Attribute_Categorical(title="New_Attribute_Categorical",question="New Question",answer_options=["Option1","Option2"])
            self.algorithm.add_attribute(new_attribute)

            print(f"New attribute '{new_attribute.title}' added.")

            self.edit_attribute(new_attribute)


        message = "What kind of attribute do you want to add?"
        choices = [
            ("Numerical", (add_attribute_numerical,())),
            ("Categorical", (add_attribute_categorical,())),
            ("<Back>", (self.show_attributes_in_navigation,()))
        ]

        chosen_answer = self.get_user_input_menu_navigation(message,choices)

        selected_function,parameters = chosen_answer
        selected_function(*parameters)

    # Function for removing attributes

    def remove_attribute(self,attribute:Attribute):
        
        confirmation = self.get_user_input_confirm("Are you sure you want to remove this attribute? (This will also remove all requirements that use this attribute.)")
        if confirmation:
            self.algorithm.remove_attribute(attribute)
            time.sleep(1)
            self.show_attributes_in_navigation()
        else:
            print(f"Attribute '{attribute.title}' not removed.")
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

        print(f"Finished questionnaire. Result: {result}")

        time.sleep(1)

        self.algorithm.reset_evaluation()
        self.open_main_menu()