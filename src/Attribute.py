from typing import List

class Attribute:
    
    def __init__(self, title: str, question:str):
        self.title = title
        self.question = question

        
class Attribute_Categorical(Attribute):
    
    def __init__(self, title: str,question:str, answer_options: List[str]):
        super().__init__(title,question)
        self.answer_options = answer_options


    def export(self) -> dict:
        return {
            'type': 'attribute_categorical',
            'title': self.title,
            'question': self.question,
            'answer_options': self.answer_options
        }
        
class Attribute_Numerical(Attribute):

    def export(self) -> dict:
        return {
            'type': 'attribute_numerical',
            'title': self.title,
            'question': self.question
        }