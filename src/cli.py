import inquirer
from typing import List
from src.attribute import Attribute, Attribute_Categorical, Attribute_Numerical
from src.requirement import Requirement,Requirement_Logical, Logical_AND, Logical_OR, Requirement_Categorical, Requirement_Numerical
from src.socialBenefit import SocialBenefit
from src.dataset import DataSet
import json
import time
from src.decisionTree import DecisionTree


class CLI:

    def __init__(self,dataset:DataSet):
        """
        Initializes the CLI object with a dataset.

        Parameters:
        - dataset (DataSet): The dataset object to be used for the CLI.
        """

        self.dataset = dataset

    def run(self):

        """
        Runs the CLI application. Starts the main menu.
        """

        self.open_main_menu()


    # Basic User Input

    def get_user_input_categorical(self,question_count:int,question: str, choices: List[str]) -> str:
        """
        Asks the user a question with a list of choices and returns the user's choice.

        Parameters:
        - question_count (int): The number of the question.
        - question (str): The question to ask the user.
        - choices (List[str]): A list of choices for the user to choose from.

        Returns:
        The user's choice.
        """

        questions = [
            inquirer.List('choice',
                        message=f"Question {question_count}: {question}",
                        choices=choices,
                    ),
        ]
        answers = inquirer.prompt(questions,theme=inquirer.themes.GreenPassion())
        return answers['choice']

    def get_user_input_numerical(self,question_count:int,question: str) -> int:
        """
        Asks the user a question with a list of choices and returns the user's choice.

        Parameters:
        - question_count (int): The number of the question.
        - question (str): The question to ask the user.

        Returns:
        The user's input.
        """
        questions = [
            inquirer.Text('choice',
                        message=f"Question {question_count}: {question}",
                    ),
        ]
        answers = inquirer.prompt(questions,theme=inquirer.themes.GreenPassion())

        return int(answers['choice'])
    
    def get_user_input_text(self,question:str) -> str:
        """
        Asks the user a question with the option for free text and returns the user's choice.

        Parameters:
        - question (str): The question to ask the user.

        Returns:
        The user's input.
        """
        questions = [
            inquirer.Text('choice',
                        message=question,
                    ),
        ]
        answers = inquirer.prompt(questions,theme=inquirer.themes.GreenPassion())
        return answers['choice']
    
    def get_user_input_confirm(self,question:str) -> bool:
        """
        Asks the user a question with the option for a yes/no answer and returns the user's choice.

        Parameters:
        - question (str): The question to ask the user.

        Returns:
        The user's confirmation.
        """
        questions = [
            inquirer.Confirm('choice',
                        message=question,
                    ),
        ]
        answers = inquirer.prompt(questions,theme=inquirer.themes.GreenPassion())
        return answers['choice']
    
    def get_user_input_checkbox(self,question:str,choices:List[str]) -> List[str]:
        """
        Asks the user a question with the option for multiple choices and returns the user's choice.

        Parameters:
        - question (str): The question to ask the user.
        - choices (List[str]): A list of choices for the user to choose from.

        Returns:
        The user's choices.
        """

        questions = [
            inquirer.Checkbox('choice',
                        message=question,
                        choices=choices,
                    ),
        ]
        answers = inquirer.prompt(questions,theme=inquirer.themes.GreenPassion())
        return answers['choice']
    
    def get_user_input_menu_navigation(self,message: str, choices: List[str]):
        """
        Asks the user a question with the option for multiple choices and returns the user's choice.
        It is meant to be used for navigation in the CLI.

        Parameters:
        - message (str): The message to display to the user.
        - choices (List[Tuple[str,Callable]]): A list of choices for the user to choose from.

        Returns:
        The user's choice.
        """
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
        '''
        Opens the main menu of the CLI.

        The main menu contains the following options:
        - Start Dialogue
        - Calculate Decision Tree
        - Edit Attributes
        - Edit Social Benefits
        - Export Data
        - Exit

        The user can select an option by typing the corresponding number and pressing enter.

        Returns:
        None        
        '''

        message = "🏡 Main Menu"

        choices = [
            ("Start Dialogue", self.start_dialogue),
            ("Calculate Decision Tree", self.calculate_decision_tree),
            ("Edit Attributes", self.show_attributes_in_navigation),
            ("Edit Social Benefits", self.show_social_benefits_in_navigation),
            ("Export Data", self.export_data),
            ("<Exit>", exit)
        ]

        chosen_answer = self.get_user_input_menu_navigation(message=message,choices=choices)

        chosen_answer()

    def calculate_decision_tree(self):
        '''
        Calculates the decision tree based on the current dataset and opens the main menu afterwards.  
        
        '''

        print("Calculating decision tree...")
        decision_tree = DecisionTree(self.dataset)
        decision_tree.fit()
        time.sleep(1)
        self.open_main_menu()

    def export_data(self):
        '''
        Exports the current dataset to a JSON file and opens the main menu afterwards.
            
        '''
        self.dataset.export()
        time.sleep(1)
        self.open_main_menu()
        
    def show_social_benefits_in_navigation(self):

        '''
        Opens the menu for selection of social benefits.

        The menu contains the following options:
        - Social Benefits
        - Add Social Benefit
        - Back

        The user can select an option by typing the corresponding number and pressing enter.

        Returns:
        None
        
        '''

        message="Social Benefits"

        choices = [(social_benefit.name, (self.edit_social_benefit,(social_benefit,))) for social_benefit in self.dataset.social_benefit_list]

        choices = sorted(choices, key=lambda x: x[0])

        choices += [("<Add Social Benefit>", (self.add_social_benefit,()))]
        choices += [("<Back>", (self.open_main_menu,()))]

        chosen_answer = self.get_user_input_menu_navigation(message,choices)

        selected_function, parameters = chosen_answer
        selected_function(*parameters)
        
    def add_social_benefit(self):
        '''
        Adds a new social benefit to the dataset and opens the menu for editing the social benefit afterwards. 

        Returns:
        None
        
        '''
            
        new_social_benefit = SocialBenefit(name="New_Social_Benefit",requirement=Logical_AND(requirements=[]))
        self.dataset.add_social_benefit(new_social_benefit)

        print(f"New social benefit '{new_social_benefit.name}' added.")

        self.edit_social_benefit(new_social_benefit)

    # Menu for editing social benefits
            
    def edit_social_benefit(self,social_benefit:SocialBenefit):

        '''
        Opens the menu for editing a social benefit.

        The menu contains the following options:
        - Edit name
        - Edit requirement-tree
        - Delete this Social Benefit
        - Back

        The user can select an option by typing the corresponding number and pressing enter.

        Returns:
        None
        
        '''
                
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

    def delete_social_benefit(self,social_benefit:SocialBenefit):

        '''
        Removes a social benefit from the dataset and opens the menu for selection of social benefits afterwards.

        Parameters:
        - social_benefit (SocialBenefit): The social benefit to be removed.

        Returns:
        None
        '''
        confirmation = self.get_user_input_confirm("Are you sure you want to remove this social benefit?")
        if confirmation:
            self.dataset.remove_social_benefit(social_benefit)
            time.sleep(1)
            self.show_social_benefits_in_navigation()
        else:
            print(f"Social benefit '{social_benefit.name}' not removed.")
            self.edit_social_benefit(social_benefit)

    # Menu for editing social benefit-name
                
    def edit_social_benefit_name(self,social_benefit:SocialBenefit):

        '''
        Opens the menu for editing the name of a social benefit.

        Parameters:
        - social_benefit (SocialBenefit): The social benefit to be edited.

        Returns:
        None
        '''

        new_name = self.get_user_input_text(question=f"Enter a new name for the social benefit '{social_benefit.name}'")
        social_benefit.name = new_name

        self.edit_social_benefit(social_benefit)

    # Menu for editing social benefit-requirement-tree
        
    def edit_social_benefit_requirement(self,social_benefit:SocialBenefit):

        '''
        Opens the menu for editing the requirement-tree of a social benefit.

        Parameters:
        - social_benefit (SocialBenefit): The social benefit to be edited.

        Returns:
        None
        '''

        def calculate_requirement_tree(requirement, list,level=0, prefix="    "):

            '''
            Recursively calculates the requirement-tree of a social benefit and appends it to a list.
            
            Parameters:
            - requirement (Requirement): The requirement to be added to the list.
            - list (List[Tuple[str,Callable]]): The list to which the requirement is added.
            - level (int): The level of the requirement in the tree.
            - prefix (str): The prefix to be added to the requirement in the tree.

            Returns:
            None
            '''

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
        
    def edit_requirement(self,requirement:Requirement,social_benefit:SocialBenefit):

        '''
        Opens the menu for editing a requirement.

        Parameters:
        - requirement (Requirement): The requirement to be edited.
        - social_benefit (SocialBenefit): The social benefit to which the requirement belongs.

        Returns:
        None
        '''

        if isinstance(requirement,Requirement_Logical):
            self.edit_requirement_logical(requirement=requirement,social_benefit=social_benefit)
        elif isinstance(requirement,Requirement_Categorical):
            self.edit_requirement_categorical(requirement=requirement,social_benefit=social_benefit)
        elif isinstance(requirement,Requirement_Numerical):
            self.edit_requirement_numerical(requirement=requirement,social_benefit=social_benefit)
        else:
            self.edit_social_benefit_requirement(social_benefit=social_benefit)

    # Menu for editing logical requirements
    
    def edit_requirement_logical(self,requirement:Requirement_Logical,social_benefit:SocialBenefit):
        
        '''
        Opens the menu for editing a logical requirement.

        Parameters:
        - requirement (Requirement_Logical): The logical requirement to be edited.
        - social_benefit (SocialBenefit): The social benefit to which the requirement belongs.

        Returns:
        None
        '''

            
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

    def add_requirement_and(self,requirement:Requirement_Logical,social_benefit:SocialBenefit):

        '''
        Adds a new logical AND requirement to the current requirement and opens the menu for editing the new requirement.

        Parameters:
        - requirement (Requirement_Logical): The logical requirement to which the new requirement is added.
        - social_benefit (SocialBenefit): The social benefit to which the requirement belongs.

        Returns:
        None
        '''

        new_logical_requirement = Logical_AND(requirements=[])

        requirement.add_requirement(new_logical_requirement)

        self.edit_social_benefit_requirement(social_benefit=social_benefit)

    def add_requirement_or(self,requirement:Requirement_Logical,social_benefit:SocialBenefit):

        '''
        Adds a new logical OR requirement to the current requirement and opens the menu for editing the new requirement.

        Parameters:
        - requirement (Requirement_Logical): The logical requirement to which the new requirement is added.
        - social_benefit (SocialBenefit): The social benefit to which the requirement belongs.

        Returns:
        None
        '''

        new_logical_requirement = Logical_OR(requirements=[])

        requirement.add_requirement(new_logical_requirement)

        self.edit_social_benefit_requirement(social_benefit=social_benefit)

    # Menu for editing concrete requirements

    def add_requirement_concrete(self,requirement:Requirement,social_benefit:SocialBenefit):

        '''
        Opens the menu for adding a concrete requirement to a logical requirement.

        Parameters:
        - requirement (Requirement): The logical requirement to which the new requirement is added.
        - social_benefit (SocialBenefit): The social benefit to which the requirement belongs.

        Returns:
        None
        '''

        def add_requirement_concrete_attribute(requirement:Requirement,social_benefit:SocialBenefit,attribute:Attribute):

            '''
            Adds a new concrete requirement to the current requirement and opens the menu for editing the new requirement.

            Parameters:
            - requirement (Requirement): The logical requirement to which the new requirement is added.
            - social_benefit (SocialBenefit): The social benefit to which the requirement belongs.
            - attribute (Attribute): The attribute to be used for the new requirement.

            Returns:
            None
            '''

            if isinstance(attribute,Attribute_Categorical):
                new_requirement = Requirement_Categorical(attribute=attribute,required_value=[attribute.answer_options[0]])
            else:
                new_requirement = Requirement_Numerical(attribute=attribute,comparison_operator='==',required_value=0)

            requirement.add_requirement(new_requirement)
            new_requirement.parent = requirement

            self.edit_requirement(new_requirement,social_benefit)
        
        message = f"Add concrete requirement to '{requirement.get_tree_string()}'"

        choices = [
            (f"{attribute.title}", (add_requirement_concrete_attribute,(requirement,social_benefit,attribute))) for attribute in self.dataset.attribute_list
        ]

        # Sort choices by attribute title
        choices = sorted(choices, key=lambda x: x[0])

        choices += [("<Back>", (self.edit_social_benefit_requirement,(social_benefit,)))]

        chosen_answer = self.get_user_input_menu_navigation(message,choices)

        selected_function,parameters = chosen_answer
        selected_function(*parameters)

    # Confirmation for removing requirements

    def remove_requirement(self,requirement:Requirement,social_benefit:SocialBenefit):

        '''
        Removes a requirement from the current requirement and opens the menu for editing the parent requirement.

        Parameters:
        - requirement (Requirement): The requirement to be removed.
        - social_benefit (SocialBenefit): The social benefit to which the requirement belongs.

        Returns:
        None
        '''

        confirmation = self.get_user_input_confirm("Are you sure you want to remove this requirement?")
        if confirmation:
            if requirement.parent is not None:
                requirement.parent.remove_requirement(requirement)
            else:
                social_benefit.remove_requirement(requirement)

        
        self.edit_social_benefit_requirement(social_benefit=social_benefit)

    def edit_requirement_categorical(self,requirement:Requirement_Categorical,social_benefit:SocialBenefit):

        '''
        Opens the menu for editing a categorical requirement.

        Parameters:
        - requirement (Requirement_Categorical): The categorical requirement to be edited.
        - social_benefit (SocialBenefit): The social benefit to which the requirement belongs.

        Returns:
        None
        '''

        message = f"Edit categorical requirement '{requirement.attribute.title}' in {requirement.required_value}'"

        choices = [
            (f"Edit required value(s): '{requirement.required_value}'", (self.edit_requirement_categorical_required_value,(requirement,social_benefit))),
            ("Delete this Requirement", (self.remove_requirement,(requirement,social_benefit))),
            ("<Back>", (self.edit_social_benefit_requirement,(social_benefit,)))
        ]

        chosen_answer = self.get_user_input_menu_navigation(message=message,choices=choices)

        selected_function,parameters = chosen_answer
        selected_function(*parameters)

    def edit_requirement_categorical_required_value(self,requirement:Requirement_Categorical,social_benefit:SocialBenefit):

        '''
        Opens the menu for editing the required value of a categorical requirement.

        Parameters:
        - requirement (Requirement_Categorical): The categorical requirement to be edited.
        - social_benefit (SocialBenefit): The social benefit to which the requirement belongs.

        Returns:
        None
        '''

        message = f"Edit required value(s) for attribute '{requirement.attribute.title}' (select with spacebar, confirm with enter)"

        choices = [f"{answer_options}" for answer_options in requirement.attribute.answer_options]

        chosen_answers = self.get_user_input_checkbox(message,choices)

        requirement.required_value = chosen_answers

        self.edit_requirement_categorical(requirement=requirement,social_benefit=social_benefit)


    # Menu for editing numerical requirements

    def edit_requirement_numerical(self,requirement:Requirement_Numerical,social_benefit:SocialBenefit):

        '''
        Opens the menu for editing a numerical requirement.

        Parameters:
        - requirement (Requirement_Numerical): The numerical requirement to be edited.
        - social_benefit (SocialBenefit): The social benefit to which the requirement belongs.

        Returns:
        None
        '''

        def edit_comparison_operator(requirement:Requirement_Numerical,social_benefit:SocialBenefit):

            '''
            
            Opens the menu for editing the comparison operator of a numerical requirement.

            Parameters:
            - requirement (Requirement_Numerical): The numerical requirement to be edited.
            - social_benefit (SocialBenefit): The social benefit to which the requirement belongs.

            Returns:
            None

            '''

            message = f"Edit comparison operator for attribute '{requirement.attribute.title}'"

            choices = [(operator,(requirement.set_comparison_operator,(operator,))) for operator in Requirement_Numerical.comparison_operators]

            chosen_answer = self.get_user_input_menu_navigation(message=message,choices=choices)

            selected_function,parameters = chosen_answer
            selected_function(*parameters)

            self.edit_requirement_numerical(requirement=requirement,social_benefit=social_benefit)

        def edit_requirement_numerical_required_value(requirement:Requirement_Numerical,social_benefit:SocialBenefit):

            '''
            Opens the menu for editing the required value of a numerical requirement.

            Parameters:
            - requirement (Requirement_Numerical): The numerical requirement to be edited.
            - social_benefit (SocialBenefit): The social benefit to which the requirement belongs.

            Returns:
            None
            '''

            # in case of a range the who numbers are entered at once, separated by a comma
            if requirement.comparison_operator == '[]':
                new_required_value = self.get_user_input_text(question=f"Enter a new required value for the attribute '{requirement.attribute.title}' (separate min and max with a comma (,))").split(',')
                new_required_value = [int(new_required_value[0]),int(new_required_value[1])]
            
            # in case of a single value only one number is entered
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

        '''
        Opens the menu for selection of attributes.

        The menu contains the following options:
        - Attributes
        - Add Attribute
        - Back

        The user can select an option by typing the corresponding number and pressing enter.

        Returns:
        None
        '''
 
        message = "Attributes"

        choices = [(attribute.title, (self.edit_attribute,(attribute,))) for attribute in self.dataset.attribute_list]

        choices = sorted(choices, key=lambda x: x[0])

        choices += [("<Add Attribute>", (self.add_attribute,()))]

        choices += [("<Back>", (self.open_main_menu,()))]

        chosen_answer = self.get_user_input_menu_navigation(message,choices)

        selected_function,parameters = chosen_answer
        selected_function(*parameters)

    # Menu for editing attributes
            
    def edit_attribute(self,attribute:Attribute):

        '''
        Opens the menu for editing an attribute.

        Parameters:
        - attribute (Attribute): The attribute to be edited.

        Returns:
        None
        '''

            
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

        '''
        Opens the menu for editing the title of an attribute.

        Parameters:
        - attribute (Attribute): The attribute to be edited.

        Returns:
        None
        '''

        new_title = self.get_user_input_text(question=f"Enter a new title for the attribute '{attribute.title}'")

        if new_title == attribute.title or new_title == "":
            print("Title not changed.")
        elif self.dataset.check_attribute_title(new_title):
            print("Title already exists.")
        else:
            attribute.title = new_title
            print(f"Title changed to '{attribute.title}'.")

        self.edit_attribute(attribute)

    # Menu for editing attribute-question
        
    def edit_attribute_question(self,attribute:Attribute):

        '''
        Opens the menu for editing the question of an attribute.

        Parameters:
        - attribute (Attribute): The attribute to be edited.

        Returns:
        None
        '''

        new_question = self.get_user_input_text(question=f"Enter a new question for the attribute '{attribute.question}'")
        attribute.question = new_question

        self.edit_attribute(attribute)

    # Menu for editing attribute-answer-options
        
    def edit_attribute_answer_options(self,attribute:Attribute):
        '''
        Opens the menu for editing the answer options of a categorical attribute.

        Parameters:
        - attribute (Attribute_Categorical): The categorical attribute to be edited.

        Returns:
        '''

        if isinstance(attribute,Attribute_Categorical):
            new_answer_options = self.get_user_input_text(question=f"Enter new answer options for the attribute, separated by a comma (,) '{attribute.title}'").split(',')
            attribute.answer_options = new_answer_options

        self.edit_attribute(attribute)

    # Menu for adding new attributes
    
    def add_attribute(self):

        '''
        Opens the menu for adding a new attribute.

        Returns:
        None
        '''

        def add_attribute_numerical():
            '''
            Adds a new numerical attribute to the dataset and opens the menu for editing the new attribute.
            '''
            new_attribute = Attribute_Numerical(title="New_Attribute_Numerical",question="New Question",min=0,max=100000)
            self.dataset.add_attribute(new_attribute)

            print(f"New attribute '{new_attribute.title}' added.")

            self.edit_attribute(new_attribute)
        
        def add_attribute_categorical():
            '''
            Adds a new categorical attribute to the dataset and opens the menu for editing the new attribute.
            '''
            new_attribute = Attribute_Categorical(title="New_Attribute_Categorical",question="New Question",answer_options=["Option1","Option2"])
            self.dataset.add_attribute(new_attribute)

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

    def remove_attribute(self,attribute:Attribute):

        '''
        Removes an attribute from the dataset and opens the menu for selection of attributes afterwards.

        Parameters:
        - attribute (Attribute): The attribute to be removed.

        Returns:
        None
        '''
        
        confirmation = self.get_user_input_confirm("Are you sure you want to remove this attribute? (This will also remove all requirements that use this attribute.)")
        if confirmation:
            self.dataset.remove_attribute(attribute)
            time.sleep(1)
            self.show_attributes_in_navigation()
        else:
            print(f"Attribute '{attribute.title}' not removed.")
            self.edit_attribute(attribute)

        
    def start_dialogue(self):

        '''
        Starts the dialogue with the user to calculate the social benefits.

        Returns:
        None
        '''

        decision_tree = DecisionTree(self.dataset)
        dataframe = self.dataset.get_dataframes()
        question_count = 1

        # Repeat until only the social benefit column is left
        while dataframe.shape[1] > 1:

            # Find the best attribute to split the dataframe
            best_attribute = decision_tree._find_best_split_attribute(dataframe=dataframe)

            if isinstance(best_attribute,Attribute_Categorical):
                answer = self.get_user_input_categorical(question_count=question_count,question=best_attribute.question,choices=best_attribute.answer_options)
            else:
                try:
                    answer = self.get_user_input_numerical(question_count=question_count,question=best_attribute.question)
                except:
                    print("Please enter a valid number.")
                    continue
            
            # Reduce the dataframe based on the user's answer
            dataframe = decision_tree._reduce_dataframe(dataframe,best_attribute,answer)

            # Increase question count
            question_count += 1
        
        # Print the result
        if len(dataframe) == 0:
            print("Result is in. From the given data, you are not eligable for any social benefit.")
        else:
            # Print the social benefits for which the user is eligable
            print(f"Result is in. From the given data, you are eligable for the following social benefits: {dataframe['social_benefit'].unique()}")

        time.sleep(1)

        self.open_main_menu()