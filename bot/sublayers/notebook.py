import pickle
from collections import UserDict
from colorama import Fore, Style, init
from prettytable import PrettyTable
init(autoreset=True)


class Notebook(UserDict):
    _instance = None
    """Storage for Notes. Saves after any changes. Loads after entering in sublayer
    """
    def __new__(cls, *args, **kwargs):

        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    file_name = 'Notebook.bin'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_notes()

    def show_all_records(self):
        return self.data

    def iterate(self, n=1):
        for key, _ in self.data.items():
            d_list = list(self.data.values())
            for i in range(0, len(d_list), n):
                yield key, d_list[i:i + n]

    def add_record(self, record):
        self.data[record.title.value] = record

    def save_notes(self):
        with open(self.file_name, 'wb') as file:
            pickle.dump(self.data, file)
        print(Style.BRIGHT+Fore.YELLOW+f'Your notes are saved!')

    def load_notes(self):
        try:
            with open(self.file_name, 'rb') as file:
                self.data = pickle.load(file)
        except:
            return


class Record:
    """Keeps all info about note
    """
    def __init__(self, title=None, text=None, tag=None):
        self.title = title
        self.text = text
        self.tags = []
        if tag:
            self.tags.append(tag)

    def add_tag(self, tag):
        self.tags.append(tag)

    def create_tag(self, record, user_tag=None, update=False):
        if user_tag:
            for _ in range(10):
                tag = Tag(user_tag)
                if update:
                    record.tags = [tag]
                else:
                    record.add_tag(tag)
                    break

    def create_text(self, record, user_text):
        text = Text(user_text)
        record.text = text

    def create_title(self, record, user_title):
        title = Title(user_title)
        record.title = title

    def formatting_record(self, record):
        title = getattr(record, 'title', '')
        if title:
            title_value = title.value
        else:
            title_value = "not found"
        text = getattr(record, 'text', '')
        if text:
            text_value = text.value
        else:
            text_value = "not found"
        tags = getattr(record, 'tags', '')
        if tags:
            tag_value = [tag.value for tag in tags]
        else:
            tag_value = "not found"

        return {"title": title_value, "text": text_value, "#tag": tag_value}


class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value


class Title(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if len(value) > 20:
            raise ValueError


class Text(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if len(value) > 150:
            raise ValueError


class Tag(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if len(value) > 5:
            raise ValueError


class CommandsHandler:
    notebook = Notebook()

    def add_note(self):
        user_title = input(Style.BRIGHT + Fore.BLUE + "Enter a title: ")
        record = Record(title=user_title)
        record.create_title(record=record, user_title=user_title)
        user_text = input(Style.BRIGHT + Fore.BLUE + "Enter a text of note: ")
        record.create_text(record=record, user_text=user_text)
        user_tag = input(Style.BRIGHT + Fore.BLUE + "Enter a #tag: ")
        record.create_tag(record=record, user_tag=user_tag)
        self.notebook.add_record(record)
        self.notebook.save_notes()

    def show_all_notes(self):
        data = self.notebook.show_all_records()
        if not data:
            print("\033[4m\033[31m{}\033[0m".format
                  ('The notebook is empty.'))
        else:
            for title, record in data.items():
                rec_data = record.formatting_record(record)
                print(Fore.GREEN + f"|Title: {title}\n"
                      f"|Text: {rec_data['text']}\n"
                      f"|Tag: {rec_data['#tag']}\n")

    def find_note(self):
        find_user = input(Style.BRIGHT+Fore.BLUE + 'Enter title or #tag: ')
        data = self.notebook.show_all_records()
        if not data:
            print("\033[4m\033[31m{}\033[0m".format
                  ('The notebook is empty.'))
        else:
            flag = False
            for title, record in data.items():
                rec_data = record.formatting_record(record)
                if title.startswith(find_user):
                    flag = True
                    print("\033[3m\033[35m{}\033[0m".format(f"|Title: {title}\n"
                          f"|Text: {rec_data['text']}\n"
                                                            f"|Tag: {rec_data['#tag']}\n"))
                tags = getattr(record, 'tags', '')
                if tags:
                    for tag in tags:
                        if tag.value.startswith(find_user):
                            flag = True
                            print("\033[3m\033[35m{}\033[0m".format(f"|Title: {title}\n"
                                  f"|Text: {rec_data['text']}\n"
                                                                    f"|Tag: {rec_data['#tag']}\n"))
            if not flag:
                print(Style.BRIGHT+Fore.RED +
                      'Note with this title or #tag was not found.')

    def sort_notes_by_tag(self):
        notes_tag = []
        notes_without_tag = []
        for name, record in self.notebook.items():
            if getattr(record, 'tags', ''):
                notes_tag.append(record)
            else:
                notes_without_tag.append(record)
        sortedDictWithTag = sorted(notes_tag, key=lambda x: len(x.tags),
                                   reverse=True)
        sortedDictWithTag.extend(notes_without_tag)
        for res in sortedDictWithTag:
            rec_data = record.formatting_record(res)
            print(Fore.GREEN + f"|Title: {rec_data['title']}\n"
                               f"|Text: {rec_data['text']}\n"
                               f"|Tag: {rec_data['#tag']}\n")

    def change_note(self):
        change_user = input(Style.BRIGHT + Fore.CYAN + 'Enter title of note: ')
        data = self.notebook.show_all_records()
        if not data:
            print("\033[4m\033[31m{}\033[0m".format
                  ('The Notebook is empty.'))
        else:
            flag = False
            update_title_data = {}
            for title, record in data.items():
                if title.startswith(change_user):
                    flag = True
                    change_commands = PrettyTable()
                    change_commands.field_names = \
                        [Style.BRIGHT + Fore.CYAN +
                         "Command entry", "Command value"]
                    change_commands.add_row(
                        [Style.BRIGHT + Fore.CYAN +
                         "Press 1", "Add tag"])
                    change_commands.add_row(
                        [Style.BRIGHT + Fore.CYAN +
                         "Press 2", "Change title of note"])
                    change_commands.add_row(
                        [Style.BRIGHT + Fore.CYAN +
                         "Press 3", "Change text"])
                    change_commands.add_row(
                        [Style.BRIGHT + Fore.CYAN +
                         "Press 4", "Change tags"])
                    print(change_commands)
                    change = int(
                        input(Style.BRIGHT + Fore.CYAN + 'Enter your choice: '))
                    if change == 1:
                        tag_add = input(
                            Style.BRIGHT + Fore.CYAN + 'Enter a tag: ')
                        record.create_tag(record=record, user_tag=tag_add,
                                          update=False)
                        print(Style.BRIGHT + Fore.YELLOW +
                              f'In note {title} append '
                              f'{[tag.value for tag in record.tags]}')
                    elif change == 2:
                        new_title = input(
                            Style.BRIGHT+Fore.CYAN + 'Enter a new title: ')
                        record.title = Title(new_title)
                        update_title_data[title] = new_title
                        print(Style.BRIGHT + Fore.YELLOW +
                              f'In note title {title} was changed to '
                              f'{record.title.value}')
                    elif change == 3:
                        text = input(Style.BRIGHT + Fore.CYAN +
                                     'Enter a new text: ')
                        record.create_text(
                            record=record, user_text=text)
                        print(Style.BRIGHT + Fore.YELLOW +
                              f'In note {title} change text '
                              f'{record.text.value}')
                    elif change == 4:
                        tag_add = input(
                            Style.BRIGHT + Fore.CYAN + 'Enter a tag: ')
                        record.create_tag(record=record, user_tag=tag_add,
                                          update=True)
                        print(Style.BRIGHT + Fore.YELLOW +
                              f'In note {title} update '
                              f'{[tag.value for tag in record.tags]}')
                    else:
                        print(Style.BRIGHT+Fore.RED +
                              f'{change} invalid choice')
            for title, new_title in update_title_data.items():
                self.notebook.data[new_title] = \
                    self.notebook.data.pop(title)
            if flag:
                self.notebook.save_notes()

    def remove_note(self):
        remove_commands = PrettyTable()
        remove_commands.field_names = ["Command entry", "Command value"]
        remove_commands.add_row(["del", "Delete one selected note"])
        remove_commands.add_row(["del all",
                                 "Delete all notes in Notebook"])
        print("\033[1m\033[31m{}\033[0m".format(remove_commands))
        remove_date = input(Style.BRIGHT + Fore.RED + 'Enter your choice: ')
        if remove_date == 'del':
            remove_note = input(Style.BRIGHT + Fore.YELLOW +
                                'Enter a title of the note to be deleted: ')
            self.notebook.data.pop(remove_note)
            print(Style.BRIGHT + Fore.RED + f'Note {remove_note} deleted.')
        elif remove_date == 'del all':
            print(Style.BRIGHT + Fore.RED +
                  f'Are you sure you want to clear the Notebook?')
            question = input(Style.BRIGHT + Fore.RED +
                             'Y or N: ').lower().strip()
            if question == 'n':
                return
            elif question == 'y':
                self.notebook.data.clear()
        self.notebook.save_notes()


# ------------------------------------------------ADAPTER-------------------------------------------------------
help = ('|You can use following commands:\n'
        '|add - add a new note in Notebook\n'
        '|del - delete a note from Notebook\n'
        '|change - change a note in Notebook\n'
        '|find - find note in Notebook\n'
        '|tag sort - sorts notes by tags in Notebook\n'
        '|show all - shows the entire Notebook\n'
        '|back - Closing the sublayer\n')

commands = {'add': CommandsHandler().add_note,
            'del': CommandsHandler().remove_note,
            'change': CommandsHandler().change_note,
            'find': CommandsHandler().find_note,
            'tag sort': CommandsHandler().sort_notes_by_tag,
            'show all': CommandsHandler().show_all_notes,
            'back': ...}

CONFIG = ({'help': help,
           'commands': commands})
