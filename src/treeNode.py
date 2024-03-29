class TreeNode:
    def __init__(self, attribute=None, social_benefits=None, children=None):
        """
        Initializes the TreeNode object with an attribute, social benefits, and children.
        Parameters:
        - attribute (Attribute): The attribute associated with the node.
        - social_benefits (List[SocialBenefit]): The social benefits associated with the node.
        - children (List[TreeNode]): The children of the node.
        """
        self.attribute = attribute
        self.social_benefits = social_benefits
        self.children = children if children is not None else []
    
    def export(self):
        """
        Converts the current node to a JSON object.
        """
        return {
            'feature': self.feature,
            'value': self.value,
            'children': [child.to_json() for child in self.children]
        }