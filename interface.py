import inquirer

from sublayers.addressbook import commands as ab_commands
from sublayers.notebook import commands as nb_commands
from sublayers.cleaner import commands as sa_commands
from sublayers.handler import Handler


main_menu = [
    inquirer.List(
        "option",
        message="You are in main menu. Please select an option:",
        choices=["Address Book", "Note Book", "Sorter Assist", "Exit"],
    )
]


def main():
    while True:
        main_choice = inquirer.prompt(main_menu)["option"]

        if main_choice == "Address Book":
            handler = Handler(ab_commands)
            handler.run()

        elif main_choice == "Note Book":
            handler = Handler(nb_commands)
            handler.run()

        elif main_choice == "Sorter Assist":
            handler = Handler(sa_commands)
            handler.run()

        elif main_choice == "Exit":
            print("Exiting program...")
            break


if __name__ == "__main__":
    main()
