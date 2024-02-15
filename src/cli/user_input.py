from typing import List, Union
import inquirer  # Ensure you have imported inquirer

def get_user_input(question_type: str, message: str, choices: List[str] = None) -> Union[str, int, bool, List[str]]:
    """
    Generalized function to get user input of various types.

    Parameters:
    - question_type (str): Type of question ('list', 'text', 'confirm', 'checkbox').
    - message (str): Message or question to display to the user.
    - choices (List[str], optional): List of choices for the user to select from. Required for 'list' and 'checkbox'.

    Returns:
    - Union[str, int, bool, List[str]]: User's input, type depends on question_type.
    """
    # Define a theme for all prompts
    theme = inquirer.themes.GreenPassion()

    # Map the question_type to the corresponding inquirer class
    question_map = {
        "list": inquirer.List,
        "text": inquirer.Text,
        "confirm": inquirer.Confirm,
        "checkbox": inquirer.Checkbox,
    }
    question_class = question_map.get(question_type)
    if not question_class:
        # If an unsupported question_type is provided, raise an error
        raise ValueError(f"Unsupported question type: {question_type}")

    # Create the question based on the provided parameters
    questions = [question_class('choice', message=message, choices=choices)]

    # Prompt the user with the question and apply the specified theme
    answers = inquirer.prompt(questions, theme=theme)

    # Return the user's answer
    return answers['choice']

# Example usage of the function
user_choice = get_user_input("text", "Choose an option:", ["Option 1", "Option 2"])
print(user_choice)