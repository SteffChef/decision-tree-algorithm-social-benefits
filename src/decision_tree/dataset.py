from typing import List

from attribute import Attribute
from socialBenefit import SocialBenefit
from datasetIo import *
import pandas as pd


class DataSet:
    def __init__(self):


        data_path = "data/exported_data/exported_data.json"

        self.attribute_list,self.social_benefit_list = load_data_from_json(data_path)

    def get_relevant_attribute_counts(self) -> List[int]:
        """
        Gibt eine Liste mit der Anzahl der verschiedenen Werte für jedes Attribut zurück.
        """
        dataset_counts = {social_benefit.name: social_benefit.get_relevant_attribute_counts() for social_benefit in self.social_benefit_list}
        
        return dataset_counts
    
    def get_dataframes(self) -> List[pd.DataFrame]:
        """
        Gibt eine Liste von DataFrames zurück, die die Anforderungen für jedes Sozialleistungselement enthalten.
        """

        dataframes = [social_benefit.get_dataframe() for social_benefit in self.social_benefit_list]

        return pd.concat(dataframes, ignore_index=True)
    
    def get_attribute_from_title(self,attribute_title: str) -> Attribute:
        for attribute in self.attribute_list:
            if attribute.title == attribute_title:
                return attribute
        return None
        
    
    def export(self):
        """
        Converts the current node to a JSON object.
        """
        # todo
        return {
            'feature': self.feature,
            'value': self.value,
            'children': [child.to_json() for child in self.children]
        }