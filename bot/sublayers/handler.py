import difflib


class Handler:
    """take CONFIG file from modules.
       Run commands, check user typos.
    """
    def __init__(self, help, commands, database=None):
        self.database = database
        self.commands = commands
        self.help = help

    def get_command_suggestion(self, query):
        return difflib.get_close_matches(query, self.commands.keys(),
                                         n=1, cutoff=0.6)

    def execute_command(self, query):
        if self.database:
            self.commands[query](self.database)
        self.commands[query]()

    def run(self):
        print(self.help)
        while True:
            query = input('> ')
            if query == 'back':
                break
            try:
                self.execute_command(query)
            except KeyError:
                suggestion = self.get_command_suggestion(query)
                if suggestion:
                    print(f'Did you mean {suggestion[0]}?')
                else:
                    print('Invalid command')
                    print(self.help)
