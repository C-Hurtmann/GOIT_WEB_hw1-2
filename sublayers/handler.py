import difflib


class Handler:
    """take CONFIG file from modules.
    Run commands, check user typos.
    """

    def __init__(self, commands):
        self.commands = commands

    def get_command_suggestion(self, query):
        return difflib.get_close_matches(query, self.commands.keys(), n=1, cutoff=0.6)

    def execute_command(self, query):
        self.commands[query]()

    def run(self):
        self.execute_command("help")
        while True:
            query = input("> ")
            if query == "back":
                break
            try:
                self.execute_command(query)
            except KeyError:
                suggestion = self.get_command_suggestion(query)
                if suggestion:
                    print(f"Did you mean {suggestion[0]}?")
                else:
                    print("Invalid command")
                    self.execute_command("help")
