from typing import List

class Attribute:
    """
    A base class for defining an attribute with a title and a question.
    """
    
    def __init__(self, title: str, question:str):
        """
        Initializes the Attribute object with a title and a question.

        Parameters:
        - title (str): The title of the attribute.
        - question (str): The question related to the attribute.
        """
        self.title = title
        self.question = question

        
class Attribute_Categorical(Attribute):
    """
    A subclass of Attribute for attributes that have categorical answers.
    """
    
    def __init__(self, title: str,question:str, answer_options: List[str]):
        """
        Initializes the Attribute_Categorical object with a title, question, and answer options.

        Parameters:
        - title (str): The title of the categorical attribute.
        - question (str): The question related to the categorical attribute.
        - answer_options (List[str]): A list of strings representing the answer options for the categorical attribute.
        """

        super().__init__(title,question)
        self.answer_options = answer_options


    def export(self) -> dict:
        """
        Exports the categorical attribute details as a dictionary.

        Returns:
        A dictionary representing the attribute with its type, title, question, and answer options.
        """
        return {
            'type': 'attribute_categorical',
            'title': self.title,
            'question': self.question,
            'answer_options': self.answer_options
        }
        
class Attribute_Numerical(Attribute):
    """
    A subclass of Attribute for attributes that are numerical.
    """
    def __init__(self, title: str, question:str, min, max):
        """
        Initializes the Attribute_Numerical object with a title and question.

        Parameters:
        - title (str): The title of the numerical attribute.
        - question (str): The question related to the numerical attribute.
        - min: The minimum value for the numerical attribute.
        - max: The maximum value for the numerical attribute.
        """
        super().__init__(title,question)
        self.min = min
        self.max = max

    def export(self) -> dict:

        """
        Exports the numerical attribute details as a dictionary.

        Returns:
        A dictionary representing the attribute with its type, title, and question.
        """
        return {
            'type': 'attribute_numerical',
            'title': self.title,
            'question': self.question,
            'min': self.min,
            'max': self.max
        }