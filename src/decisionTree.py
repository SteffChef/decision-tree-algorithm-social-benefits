from typing import Any, List, Optional, Tuple, Dict
from src.treeNode import TreeNode
from src.dataset import DataSet
from math import log2
from collections import Counter
from src.attribute import Attribute, Attribute_Numerical, Attribute_Categorical
import pandas as pd

class DecisionTree:
    '''
    A class for representing a decision tree.

    Attributes:
    - dataset (DataSet): The dataset to build the decision tree on.
    - root (TreeNode): The root node of the decision tree.
    - max_depth (Optional[int]): The maximum depth of the tree. None for no limit.
    - current_max_depth (int): The current maximum depth of the tree.
    - leaf_depths (List[int]): A list of all leaf depths in the tree.

    Methods:
    - fit(): Fits the decision tree on the training data.
    - _build_tree(dataframe, depth, single_step): Recursively builds the decision tree from the training data.
    - _calculate_leaf_node(dataframe, depth): Calculates the leaf node of the decision tree based on the given dataset.
    - _entropy(dataframe): Calculates the entropy of the given dataset.
    - _gain_ratio(dataframe, attribute_name, current_entropy): Calculates the gain ratio of the given attribute in the given dataset.
    - _check_numeric_range_or_nan(row, attribute_name, value): Checks if the given row falls within the given numeric range or is NaN.
    - _find_best_split_attribute(dataframe): Finds the best attribute to split on based on the given dataset.
    - _split(dataframe, attribute): Splits the data into two subsets based on the given feature and threshold.
    - _reduce_dataframe(dataframe, attribute, value): Reduces the given dataset by removing the given feature.
    - get_interval_values(expressions, attribute): Gets the interval values for the given attribute based on the given expressions.
    - predict(X): Predicts the class labels or target values for the given input samples.
    '''

    def __init__(self, dataset:DataSet,max_depth: Optional[int] = None):
        """Initializes a DecisionTree.

        Keyword arguments:
        max_depth: The maximum depth of the tree. None for no limit.
        """
        self.dataset = dataset
        self.root = None
        self.max_depth = max_depth
        self.current_max_depth = 0
        self.leaf_depths = []

    def fit(self) -> None:
        
        """Fits the decision tree on the training data.

        Args:
            X: The training input samples. Each entry is a list of feature values.
            y: The target values (class labels for classification, real numbers for regression).
        """
        self.root = self._build_tree(self.dataset.get_dataframes(),depth=1)

        average_depth = sum(self.leaf_depths)/len(self.leaf_depths)

        print('Tree built successfully.')
        print(f"Max depth: {max(self.leaf_depths)}")
        print(f"Average depth: {average_depth}")
        print(f"Total leaf nodes: {len(self.leaf_depths)}")


    def _build_tree(self,dataframe,  depth: int ) -> TreeNode:

        # pre-pruning
        if self.max_depth is not None and depth >= self.max_depth:
            return self._calculate_leaf_node(dataframe,depth)
        

        #if the dataset is either empty or contains only class labels, return a leaf node with all class label
        if len(dataframe) == 0 or len(dataframe.columns) == 1:
            return self._calculate_leaf_node(dataframe,depth)
        
        best_attribute = self._find_best_split_attribute(dataframe)

        if best_attribute is None:
            return self._calculate_leaf_node(dataframe,depth)
        
        # create a new tree node with the best attribute
        node = TreeNode(attribute=best_attribute)

        # split the dataset based on the best attribute
        split_dataframes = self._split(dataframe,best_attribute)

        # recursively build the subtree
        for reduced_dataframe in split_dataframes:
            node.children.append(self._build_tree(reduced_dataframe, depth + 1))

        """Recursively builds the decision tree from the training data.



        Args:
            X: The training input samples at the current node.
            y: The target values at the current node.
            depth: The current depth of the tree.

        Returns:
            The root node of the constructed decision tree.
        """

    
    def _calculate_leaf_node(self,dataframe:DataSet,depth) -> TreeNode:
        '''
        Calculates the leaf node of the decision tree based on the given dataset.

        Parameters:
        - dataframe (DataSet): The dataset at the current node.
        - depth (int): The depth of the current node.

        Returns:
        - TreeNode: The leaf node of the decision tree.        
        '''

        # calculate the remaining classes class label
        self.leaf_depths.append(depth)

        # update the current max depth
        if depth > self.current_max_depth:
            self.current_max_depth = depth

        # if the dataset is empty, return a leaf node with no class label
        if len(dataframe) == 0:
            return TreeNode(social_benefits=[])
        else:
            # return a leaf node with the remaining class label
            return TreeNode(social_benefits=dataframe['social_benefit'].unique())

        # calculate the most common class label

        
    
        
    def _check_numeric_range_or_nan(self,row,attribute_name,value):

        if pd.isna(row[attribute_name]):
            return True 
        return row[attribute_name][0] <= value <= row[attribute_name][1] 

    
    def _find_best_split_attribute(self, dataframe:DataSet,selection_method:str = None) -> Dict:

        # Calculation of the attribute reduction

        attributes = [attribute_name for attribute_name in dataframe.columns if attribute_name != 'social_benefit']
        
        if selection_method == None:
            best_split_attribute = None
            best_average_column_count = 100000

            for attribute in attributes:
                attribute = self.dataset.get_attribute_from_title(attribute)
                split_dataframes = self._split(dataframe,attribute)
                current_column_count = sum(len(df.columns) for df in split_dataframes)/len(split_dataframes)
                if current_column_count < best_average_column_count:
                    best_average_column_count = current_column_count
                    best_split_attribute = attribute

            return best_split_attribute
    
        """Finds the best attribute to split on based on the given dataset.

        Args:
            data_set: The dataset for which the best attribute is to be found.

        Returns:
            A tuple containing the index of the best attribute and the corresponding gain ratio.
        """
        # Logic for finding the best attribute goes here.
        
        

    def _split(self, dataframe:pd.DataFrame, attribute:Attribute) -> Any:
        """Splits the data into two subsets based on the given feature and threshold.

        Args:
            X: The input samples.
            y: The target values.
            feature_index: The index of the feature to split on.
            threshold: The threshold value to split the samples.

        Returns:
            Two tuples containing the input samples and target values for the two subsets.
        """
        # Logic for splitting the data goes here.

        # calculate 
        if isinstance(attribute,Attribute_Numerical):
            interval_values = self._get_interval_values(dataframe[attribute.title].dropna(),attribute)
            return [self._reduce_dataframe(dataframe, attribute, value) for value in interval_values]
        
        else:
            return [self._reduce_dataframe(dataframe, attribute, value) for value in attribute.answer_options]


    def _reduce_dataframe(self, dataframe, attribute:Attribute, value: Any) -> Any:
        """Reduces the given dataset by removing the given feature.

        Args:
            X: The input samples.
            y: The target values.
            feature_index: The index of the feature to remove.

        Returns:
            The input samples with the given feature removed.
        """
        # Logic for reducing the data goes here.
        if isinstance(attribute,Attribute_Numerical):
            mask = dataframe.apply(self._check_numeric_range_or_nan, axis=1, args=(attribute.title, value))
            reduced_dataframe = dataframe[mask].drop(columns=[attribute.title])
        # if the attribute is categorical, remove all rows that don't have the given value 
        else:
            filter_criteria = pd.isna(dataframe[attribute.title]) | (dataframe[attribute.title] == value)
            reduced_dataframe = dataframe[filter_criteria].drop(columns=[attribute.title])

        # remove all columns that have all NaN values
        return reduced_dataframe.dropna(axis=1, how='all')
        

    def _get_interval_values(self,expressions,attribute:Attribute) -> List[float]:

        '''
        Gets the interval values for the given attribute based on the given expressions.

        Parameters:
        - expressions (List[Tuple[float,float]]): The expressions for the attribute.
        - attribute (Attribute): The attribute to get the interval values for.

        Returns:
        - List[float]: The interval values for the attribute.

        '''

        interval_values = set()
        
        lower_bounds = set()
        upper_bounds = set()

        for exp in expressions:
            lower, upper = exp
            lower_bounds.add(lower)
            upper_bounds.add(upper)

        #if min of attribute is not in lower bounds, add it
        if attribute.min not in lower_bounds:
            lower_bounds.add(attribute.min)
        
        #if max of attribute is not in upper bounds, add it
        if attribute.max not in upper_bounds:
            upper_bounds.add(attribute.max)

        # while both sets are not empty

        last = None
        while lower_bounds and upper_bounds:
            lower = min(lower_bounds)
            upper = min(upper_bounds)
            
            if lower < upper:
                interval_values.add((upper + lower)/2)
                lower_bounds.remove(lower)
                last = lower
                continue
            if lower == upper:
                interval_values.add(lower)
                upper_bounds.remove(upper)
                continue
            if lower > upper:
                interval_values.add((upper + lower)/2)
                upper_bounds.remove(upper)
        
        while upper_bounds:
            upper = min(upper_bounds)
            interval_values.add((upper + last)/2)
            last = upper
            upper_bounds.remove(upper)
            
        return interval_values