from typing import Any, List, Optional, Tuple, Dict
from treeNode import TreeNode
from dataset import DataSet
from math import log2
from collections import Counter
from attribute import Attribute, Attribute_Numerical, Attribute_Categorical
import pandas as pd

class DecisionTree:
    """Implementation of a decision tree for classification or regression.

    Attributes:
        root (Optional[TreeNode]): The root node of the decision tree.
        max_depth (Optional[int]): The maximum depth of the tree.
    """
    """Form a complex number.

    Keyword arguments:
    real -- the real part (default 0.0)
    imag -- the imaginary part (default 0.0)
    """

    def __init__(self, dataset:DataSet,max_depth: Optional[int] = None):
        """Initializes a DecisionTree.

        Keyword arguments:
        max_depth: The maximum depth of the tree. None for no limit.
        """
        self.dataset = dataset
        self.root = None
        self.max_depth = max_depth
        self.current_max_depth = 0
        self.current_average_depth = 0

    def fit(self) -> None:
        
        """Fits the decision tree on the training data.

        Args:
            X: The training input samples. Each entry is a list of feature values.
            y: The target values (class labels for classification, real numbers for regression).
        """
        self.root = self._build_tree(depth=1)

    def step(self) -> None:
        """Fits the decision tree on the training data.

        Args:
            X: The training input samples. Each entry is a list of feature values.
            y: The target values (class labels for classification, real numbers for regression).
        """
        self.root = self._build_tree(dataset=self.dataset, depth=1,single_step=True)

    def _build_tree(self,dataframe,  depth: int ,single_step = False) -> TreeNode:

        # pre-pruning
        if self.max_depth is not None and depth >= self.max_depth:
            return self._calculate_leaf_value(y)

        #if the dataset is either empty or contains only class labels, return a leaf node with all class label
        if len(dataframe) == 0 or len(dataframe.columns) == 1:
            return self._calculate_leaf_value(dataframe)
        """Recursively builds the decision tree from the training data.



        Args:
            X: The training input samples at the current node.
            y: The target values at the current node.
            depth: The current depth of the tree.

        Returns:
            The root node of the constructed decision tree.
        """
        # Logic for building the tree goes here.
        if single_step:
            return TreeNode()
        
    def _entropy(self,dataframe) -> float:

        """Calculates the entropy of the given dataset.

        Args:
            data_set: The dataset for which entropy is to be calculated.

        Returns:
            The entropy of the dataset.
        """
        total_length = len(dataframe)
        counts = Counter([label for label in dataframe['social_benefit']])

        # Application of the entropy formula
        return sum((-count/total_length) * log2(count/total_length) for count in counts.values())
    
    def _gain_ratio(self, dataframe:DataSet, attribute_name:str,current_entropy:float) -> float:
        """Calculates the gain ratio of the given attribute in the given dataset.

        Args:
            data_set: The dataset for which the gain ratio is to be calculated.
            attribute_index: The index of the attribute for which the gain ratio is to be calculated.

        Returns:
            The gain ratio of the attribute.
        """

        # find out all the possible attribute values
        attribute = self.dataset.get_attribute_from_title(attribute_name)

        if isinstance(attribute,Attribute_Numerical):
            attribute_values = self.get_interval_values(dataframe[attribute_name].dropna(),attribute)

            # calculate the split entropy
            split_entropy = 0
            for value in attribute_values:
                mask = dataframe.apply(self._check_numeric_range_or_nan, axis=1, args=(attribute_name, value))
                reduced_dataframe = dataframe[mask].drop(columns=[attribute_name])
                split_entropy += self._entropy(reduced_dataframe) * len(reduced_dataframe)/len(dataframe)

            # calculate the gain ratio
            gain = current_entropy - split_entropy
            # split_info = -sum((len(dataframe[dataframe[attribute_name][0] <= value <=dataframe[attribute_name]])/len(dataframe)) * log2(len(dataframe[dataframe[attribute_name][0] <= value <=dataframe[attribute_name]])/len(dataframe) + 1e-10) for value in attribute_values)
            split_info = 0
            for value in attribute_values:
                mask = dataframe.apply(self._check_numeric_range_or_nan, axis=1, args=(attribute_name, value))
                reduced_dataframe = dataframe[mask].drop(columns=[attribute_name])
                split_info += len(reduced_dataframe)/len(dataframe) * log2(len(reduced_dataframe)/len(dataframe) + 1e-10)
                
            return gain / (-split_info) if split_info != 0 else 0
        else:
            attribute_values = attribute.answer_options

            # calculate the split entropy
            split_entropy = 0
            for value in attribute_values:
                reduced_dataframe = dataframe[(dataframe[attribute_name].isna() | dataframe[attribute_name] == value)].drop(columns=[attribute_name])
                split_entropy += self._entropy(reduced_dataframe) * len(reduced_dataframe)/len(dataframe)

            # calculate the gain ratio
            gain = current_entropy - split_entropy
            split_info = -sum((len(dataframe[dataframe[attribute_name] == value])/len(dataframe)) * log2(len(dataframe[dataframe[attribute_name] == value])/len(dataframe) + 1e-10) for value in attribute_values)
            return gain / split_info if split_info != 0 else 0
        
    def _check_numeric_range_or_nan(self,row,attribute_name,value):

        if pd.isna(row[attribute_name]):
            return True 
        return row[attribute_name][0] <= value <= row[attribute_name][1] 

    
    def _find_best_split_attribute(self, dataframe:DataSet) -> Dict:

        attribute_names = [attribute_name for attribute_name in dataframe.columns if attribute_name != 'social_benefit']

        best_gain_ratio = -1
        best_split_attribute = None

        current_entropy = self._entropy(dataframe)

        for attribute_name in attribute_names:
            current_gain_ratio = self._gain_ratio(dataframe, attribute_name, current_entropy)
            print(current_entropy, current_gain_ratio, attribute_name)
            if current_gain_ratio > best_gain_ratio:
                best_gain_ratio = current_gain_ratio
                best_split_attribute = attribute_name
        
        return best_split_attribute, best_gain_ratio
        """Finds the best attribute to split on based on the given dataset.

        Args:
            data_set: The dataset for which the best attribute is to be found.

        Returns:
            A tuple containing the index of the best attribute and the corresponding gain ratio.
        """
        # Logic for finding the best attribute goes here.
        
        

    def _split(self, dataframe, attribute:Attribute) -> Any:
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
            interval_values = self.get_interval_values(dataframe[attribute.title].dropna(),attribute)
            split_dataframes = []
            for value in interval_values:
                mask = dataframe.apply(self._check_numeric_range_or_nan, axis=1, args=(attribute.title, value))
                reduced_dataframe = dataframe[mask]
                split_dataframes.append(reduced_dataframe)
            return split_dataframes
        
        else:
            split_dataframes = []
            for value in attribute.answer_options:
                reduced_dataframe = dataframe[(dataframe[attribute.title].isna() | dataframe[attribute.title] == value)]
                split_dataframes.append(reduced_dataframe)
            return split_dataframes

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
        attribute = self.dataset.get_attribute_from_title(attribute)
        if isinstance(attribute,Attribute_Numerical):
            mask = dataframe.apply(self._check_numeric_range_or_nan, axis=1, args=(attribute.title, value))
            reduced_dataframe = dataframe[mask].drop(columns=[attribute.title])
        else:
            reduced_dataframe = dataframe[(dataframe[attribute.title].isna() | dataframe[attribute.title] == value)].drop(columns=[attribute.title])

        # remove all columns that have all NaN values
        return reduced_dataframe.dropna(axis=1, how='all')
        

    def get_interval_values(self,expressions,attribute:Attribute) -> List[float]:
        print(expressions)

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

        print(lower_bounds, upper_bounds)
        # while both sets are not empty

        last = None
        while lower_bounds and upper_bounds:
            print(lower_bounds, upper_bounds)
            print(interval_values)
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

    def predict(self, X: List[List[float]]) -> List[Any]:
        """Predicts the class labels or target values for the given input samples.
# 
        Args:
            X: The input samples for which predictions are to be made.

        Returns:
            A list of predicted values or class labels.
        """
        # Logic for making predictions goes here.
        pass

    # Additional methods like _calculate_leaf_value, _split, etc., should also include comments