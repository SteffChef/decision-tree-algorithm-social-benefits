def navigate_menu(self, message: str, choices: list):
    """
    General method to navigate through menus.

    Parameters:
    - message (str): Menu prompt message.
    - choices (list): List of tuples with menu choices and corresponding actions.
    """
    # Sort choices by name if applicable
    choices = sorted(choices, key=lambda x: x[0])

    # Add common choices like Back or Exit if not already included
    if "<Back>" not in [choice[0] for choice in choices]:
        choices.append(("<Back>", self.open_main_menu))
    if "<Exit>" not in [choice[0] for choice in choices]:
        choices.append(("<Exit>", exit))

    chosen_answer = self.get_user_input_menu_navigation(message=message, choices=choices)

    # Execute the chosen action
    if callable(chosen_answer):
        chosen_answer()
    else:
        selected_function, parameters = chosen_answer
        selected_function(*parameters)