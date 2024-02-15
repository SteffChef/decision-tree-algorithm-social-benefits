def evaluate_logic(expression, x):
    """
    Evaluates a logic expression against an integer x.
    
    Parameters:
    - expression: A string containing the logic expression.
    - x: An integer to evaluate the expression against.
    
    Returns:
    - The result of the logic evaluation.
    """
    # Replace 'x' with '{}', so we can use .format(x) safely
    expression = expression.replace('x', '{}')
    
    # Use .format to safely insert x into the expression
    expression_formatted = expression.format(x)
    
    # Evaluate the expression
    return eval(expression_formatted)

# Example usage
expressions = ['<= 10', '15<=x<=17']
x = 16

for exp in expressions:
    result = evaluate_logic(exp, x)
    print(f"Expression '{exp}' with x={x}: {result}")