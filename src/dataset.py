from typing import List

from src.attribute import Attribute
from src.socialBenefit import SocialBenefit
import src.datasetIo as io
import pandas as pd


class DataSet:

    '''
    The class DataSet is the main class of the application. It contains all the attributes and social benefits and provides methods to manipulate them.

    '''

    def __init__(self):


        data_path = "data/exported_data/exported_data.json"

        self.attribute_list,self.social_benefit_list = io.load_data_from_json(data_path)
    
    def get_dataframes(self) -> List[pd.DataFrame]:
        """
        Returns a list of dataframes, where each dataframe contains the relevant attributes for a social benefit.

        Returns:
        List[pd.DataFrame]: A list of dataframes.
        """

        dataframes = [social_benefit.get_dataframe() for social_benefit in self.social_benefit_list]

        return pd.concat(dataframes, ignore_index=True)
    
    def get_attribute_from_title(self,attribute_title: str) -> Attribute:

        '''
        Returns the attribute with the given title.

        Parameters:
        - attribute_title (str): The title of the attribute to return.

        Returns:
        Attribute: The attribute with the given title, or None if no attribute with the given title exists.

        '''

        for attribute in self.attribute_list:
            if attribute.title == attribute_title:
                return attribute
        return None
        
    
    def export(self):
        """
        Converts the current node to a JSON object.
        """
        io.export_data_to_json(self.attribute_list,self.social_benefit_list)

    def add_social_benefit(self,social_benefit: SocialBenefit) -> None:

        '''
        Adds a social benefit to the dataset.

        Parameters:
        - social_benefit (SocialBenefit): The social benefit to add.

        '''


        self.social_benefit_list.append(social_benefit)
        self.set_relevant_attributes()
        print(f"Social Benefit {social_benefit.name} successfully added.")

    def remove_social_benefit(self,social_benefit: SocialBenefit) -> None:

        '''
        Removes a social benefit from the dataset.

        Parameters:
        - social_benefit (SocialBenefit): The social benefit to remove.

        '''

        self.social_benefit_list.remove(social_benefit)
        self.set_relevant_attributes()
        print(f"Social Benefit {social_benefit.name} successfully removed.")

    def add_attribute(self,attribute: Attribute) -> None:
            
        '''
        Adds an attribute to the dataset.

        Parameters:
        - attribute (Attribute): The attribute to add.

        '''

        if self.check_attribute_title(attribute.title):
            print(f"Attribute {attribute.title} already exists.")
            return
        self.attributes.append(attribute)

    def remove_attribute(self,attribute: Attribute):
        '''
        Removes an attribute from the dataset.

        Parameters:
        - attribute (Attribute): The attribute to remove.

        '''

        self.attribute_list.remove(attribute)
        for social_benefit in self.social_benefit_list:
            social_benefit.remove_requirement_by_attribute(attribute)
        print(f"Attribute {attribute.title} successfully removed.")
    
    def check_attribute_title(self,title: str) -> bool:

        '''
        Returns True if an attribute with the given title exists, False otherwise.

        Parameters:
        - title (str): The title of the attribute to check.

        Returns:
        bool: True if an attribute with the given title exists, False otherwise.

        '''
        for attribute in self.attribute_list:
            if attribute.title == title:
                return True
        return False