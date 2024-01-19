import inquirer

def open_main_menu():

    menu_questions = [
        inquirer.List("choice",
                    message="Main Menu",
                    choices=[
                        ("Start Dialogue", exit),
                        ("Edit Social Benefits", exit),
                        ("Edit Attributes", exit),
                        ("Exit", exit)
                    ],
                    ),
    ]

    selected_option = inquirer.prompt(menu_questions, theme=inquirer.themes.GreenPassion())
    print(selected_option)
    selected_option['choice']()


class Test:

    @staticmethod
    def get_user_input_menu_navigation(message,choices):
        questions = [
            inquirer.List("choice",
                        message=message,
                        choices=choices,
                        ),
        ]
        selected_option = inquirer.prompt(questions, theme=inquirer.themes.GreenPassion())
        selected_option['choice']()
        

if __name__ == "__main__":
    message = "Main Menu"
    choices = [
        ("Start Dialogue", exit),
        ("Edit Social Benefits", exit),
        ("Edit Attributes", exit),
        ("Exit", exit)
    ]
    Test.get_user_input_menu_navigation(message,choices)
