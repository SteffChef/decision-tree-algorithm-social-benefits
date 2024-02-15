class TreeNode:
    def __init__(self, feature=None, value=None, children=None):
        """
        Initialisiert einen Knoten im Entscheidungsbaum.
        :param feature: Der Index des Features, nach dem in diesem Knoten geteilt wird.
        :param value: Der Vorhersagewert oder die Klasse, wenn dies ein Blattknoten ist.
        :param children: Eine Liste von Kindknoten, wobei jeder Knoten ein Tuple aus (Schwellenwert, Kindknoten) ist.
        """
        self.attribute = feature
        self.value = value
        self.children = children if children is not None else []

    def is_leaf_node(self):
        """
        Checks, if the current node is a leaf node.
        """
        return self.value is not None
    
    def to_json(self):
        """
        Converts the current node to a JSON object.
        """
        return {
            'feature': self.feature,
            'value': self.value,
            'children': [child.to_json() for child in self.children]
        }