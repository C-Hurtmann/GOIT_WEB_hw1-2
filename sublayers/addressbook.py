from abc import abstractmethod, ABC
import pickle
from collections import UserDict
from datetime import datetime, timedelta
import re
from colorama import init, Fore, Back, Style
from prettytable import PrettyTable, ALL

init(autoreset=True)


class AddressBook(UserDict):
    """Storage for Records. Saves after any changes. Loads after entering in sublayer"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    file_name = "AddressBook.bin"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_contacts()

    def show_all_records(self):
        return self.data

    def add_record(self, record):
        self.data[record.name.value] = record

    def save_contacts(self):
        with open(self.file_name, "wb") as f:
            pickle.dump(self.data, f)
        print(Style.BRIGHT + Fore.YELLOW + f"Your contact saved!")

    def load_contacts(self):
        try:
            with open(self.file_name, "rb") as f:
                self.data = pickle.load(f)
        except:
            return


class Record:
    """Keeps all info about users contact"""

    def __init__(self, name, phone=None, email=None, birthday=None, home_address=None):
        self.name = name
        self.email = email
        self.birthday = birthday
        self.phones = []
        self.home_address = home_address
        if phone:
            self.phones.append(phone)

    def add_phone(self, phone):
        """Adds new phone to the Record if phones field not empty"""
        self.phones.append(phone)

    def create_phone(self, record, user_input=None, update=False):
        """Adds phone to the Record due it's initialization"""
        if user_input:
            for i in range(10):
                phone = Phone(user_input)
                if phone.validate_phone(user_input):
                    if update:
                        record.phones = [phone]
                    else:
                        record.add_phone(phone)
                    break
                else:
                    print(
                        Style.BRIGHT + Fore.RED + "Incorrect phone number "
                        "format entered.\n"
                        "Enter your phone in the format '+380991122333'"
                    )
                    user_input = input(
                        Style.BRIGHT + Fore.BLUE + "Enter contact phone: "
                    )

    def create_email(self, record, user_email):
        """Adds email to the Record due it's initialization"""
        if user_email:
            for i in range(10):
                email = Email(user_email)
                if email.validate_email(user_email):
                    record.email = email
                    break
                else:
                    print(
                        Style.BRIGHT + Fore.RED + "Email entered incorrectly.\n"
                        "Please enter a valid email: 'example@gmail.com'"
                    )
                    user_email = input(
                        Style.BRIGHT + Fore.BLUE + "Enter contact email: "
                    )

    def create_birthday(self, record, user_birthday):
        """Adds birthday date to the Record due it's initialization"""
        if user_birthday:
            for i in range(10):
                birthday = Birthday(user_birthday)
                if birthday.validate_birthday(user_birthday):
                    record.birthday = birthday
                    break
                else:
                    print(
                        Style.BRIGHT + Fore.RED + "Birthday invalid.\n"
                        "Birthday should be in the format\n"
                        "'day.month.year' and less than current date."
                    )
                    user_birthday = input(
                        Style.BRIGHT + Fore.BLUE + "Enter contact Birthday: "
                    )

    def home_address_create(self, record, user_address):
        """Adds home address to the Record due it's initialization"""
        if user_address:
            home_address = HomeAddress(user_address)
            record.home_address = home_address

    def formatting_record(self, record):
        """Collects all info of the Record

        Returns:
            dict: dict with all Reccord info. If somethig is empty fills 'atr is missing'
        """
        phones = getattr(record, "phones", "")
        if phones:
            p_l = [phone.value for phone in phones]
            phone_val = p_l
        else:
            phone_val = "Phone number missing."
        email = getattr(record, "email", "")
        if email:
            email_val = email.value
        else:
            email_val = "Email is missing."
        birthday = getattr(record, "birthday", "")
        if birthday:
            birthday_val = birthday.value
        else:
            birthday_val = "Date of birth is missing."
        home_address = getattr(record, "home_address", "")
        if home_address:
            home_address_val = home_address.value
        else:
            home_address_val = "Home address is missing."

        return {
            "phone": phone_val,
            "email": email_val,
            "birthday": birthday_val,
            "home_address": home_address_val,
        }


class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def __str__(self):
        return f"{self._value}"


class Name(Field):
    pass


class Phone(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not value.startswith("+"):
            raise ValueError
        if len(value) != 13:
            raise ValueError

    def validate_phone(self, phone):
        pattern = (
            r"^[\+]?3?[\s]?8?[\s]?\(?0\d{2}?\)?" r"[\s]?\d{3}[\s|-]?\d{2}[\s|-]?\d{2}$"
        )
        a = re.match(pattern, phone)
        if a is not None:
            return phone


class Email(Field):
    def validate_email(self, email):
        pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"
        a = re.match(pattern, email)
        if a is not None:
            return email


class Birthday(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def set_value(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except:
            raise ValueError

    def validate_birthday(self, birthday):
        try:
            bt_obj = datetime.strptime(birthday, "%d.%m.%Y")
            if bt_obj.date() >= datetime.now().date():
                return None
            return birthday
        except:
            pass


class HomeAddress(Field):
    pass


class CommandsHandler:
    """Needs for keeping AddressBook for all commands
    All methods of this class goes to commands dict in CONFIG
    """

    def __init__(self):
        self.address_book = AddressBook()

    def get_help(self):
        """Shows all commands for the sublayer"""
        help_string = HelpOutput()
        help_string.create_header("You can use following commands:")
        help_string.convert_data_to_table(commands)
        print(help_string)

    def add_contacts(self):
        """Add new contact"""
        user_name = input(Style.BRIGHT + Fore.BLUE + "Enter contact name: ")
        if not user_name:
            print("\033[4m\033[31m\033[45m{}\033[0m".format("Contact name is required"))
            return
        else:
            name = Name(user_name)
        record = Record(name)

        user_phone = input(Style.BRIGHT + Fore.BLUE + "Enter contact phone: ")
        record.create_phone(record=record, user_input=user_phone, update=True)

        user_email = input(Style.BRIGHT + Fore.BLUE + "Enter contact email: ")
        record.create_email(record=record, user_email=user_email)

        user_birthday = input(Style.BRIGHT + Fore.BLUE + "Enter contact Birthday: ")
        record.create_birthday(record=record, user_birthday=user_birthday)

        user_home_address = input(
            Style.BRIGHT + Fore.BLUE + "Enter contact home address: "
        )
        record.home_address_create(record=record, user_address=user_home_address)
        self.address_book.add_record(record)
        self.address_book.save_contacts()

    def show_all_contacts(self):
        data = self.address_book.show_all_records()
        if not data:
            print(
                "\033[4m\033[31m\033[45m{}\033[0m".format("The address book is empty.")
            )
        else:
            for name, record in data.items():
                rec_data = record.formatting_record(record)
                print(
                    Fore.GREEN + f"|Name: {name}, Phone: {rec_data['phone']}, "
                    f"Email: {rec_data['email']}, "
                    f"Birthday: {rec_data['birthday']},"
                    f"Home address: {rec_data['home_address']}|"
                )

    def show_all(self):
        """Shows the entire Address Book"""
        data = self.address_book.data
        table = AddressBookDataOutput()
        table.create_header(["Name", "Phones", "Email", "Birthday", "Address"])
        table.convert_data_to_table(data)
        print(Fore.GREEN + str(table))

    def find_contacts(self):
        """Find contact in Address Book"""
        find_user = input(Style.BRIGHT + Fore.BLUE + "Enter contact name or phone: ")
        data = self.address_book.show_all_records()
        if not data:
            print(
                "\033[4m\033[31m\033[45m{}\033[0m".format("The address book is empty.")
            )
        else:
            flag = False
            for name, record in data.items():
                rec_data = record.formatting_record(record)
                if name.startswith(find_user):
                    flag = True
                    find_list = (
                        f"|Name: {name}, Phone: {rec_data['phone']},"
                        f"Email: {rec_data['email']},"
                        f"Birthday: {rec_data['birthday']},"
                        f"Home address: {rec_data['home_address']}|"
                    )
                    print("\033[1m\033[35m{}\033[0m".format(find_list))
                phones = getattr(record, "phones", "")

                if phones:
                    for phone in phones:
                        if phone.value.startswith(find_user):
                            flag = True
                            print(
                                f"Name: {name}, Phone: {rec_data['phone']}, "
                                f"Email: {rec_data['email']}, "
                                f"Birthday: {rec_data['birthday']}"
                            )
            if not flag:
                print(
                    "\033[4m\033[31m\033[45m{}\033[0m".format(
                        "Contact with this name or phone number was " "not found."
                    )
                )

    def birthday_contacts(self):
        """Show birthdays"""
        birth_user = int(input(Style.BRIGHT + Fore.BLUE + "Enter a number of days: "))
        flag = False
        now = datetime.now().date()
        data = self.address_book.show_all_records()
        current_date = now + timedelta(days=birth_user)
        for name, record in data.items():
            rec_data = record.formatting_record(record)
            if record.birthday:
                birth = rec_data["birthday"]
                new_user_date = datetime.strptime(birth, "%d.%m.%Y").date()
                new_date = datetime(
                    day=new_user_date.day, month=new_user_date.month, year=now.year
                ).date()
                if new_date >= now and new_date < current_date:
                    flag = True
                    print(
                        f"Name: {name}, Phone: {rec_data['phone']}, "
                        f"Email: {rec_data['email']}, "
                        f"Birthday: {rec_data['birthday']}"
                    )
        if not flag:
            print(
                "\033[4m\033[31m\033[45m{}\033[0m".format(
                    "There are no birthdays in this range!"
                )
            )

    def change_contacts(self):
        """Change contact"""
        change_user = input(Style.BRIGHT + Fore.CYAN + "Enter contact name: ")
        data = self.address_book.show_all_records()
        if not data:
            print(
                "\033[4m\033[31m\033[45m{}\033[0m".format("The address book is empty.")
            )
        else:
            flag = False
            update_name_data = {}
            for name, record in data.items():
                if name.startswith(change_user):
                    flag = True
                    change_commands = PrettyTable()
                    change_commands.field_names = ["Command entry", "Command value"]
                    change_commands.add_row(
                        ["Press 1", "Add a phone number to a contact"]
                    )
                    change_commands.add_row(["Press 2", "Change contact email"])
                    change_commands.add_row(["Press 3", "Change contact birthday"])
                    change_commands.add_row(["Press 4", "Change contact name"])
                    change_commands.add_row(["Press 5", "Change contact phone number"])
                    change_commands.add_row(["Press 6", "Change contact home address"])
                    print("\033[1m\033[36m{}\033[0m".format(change_commands))
                    change = input(Style.BRIGHT + Fore.CYAN + "Enter your choice: ")
                    if change == "1":
                        num = input(Style.BRIGHT + Fore.CYAN + "Enter number: ")
                        record.create_phone(record=record, user_input=num, update=False)
                        print(
                            Style.BRIGHT
                            + Back.BLUE
                            + Fore.RED
                            + f"In contact {name} append "
                            f"{[phone.value for phone in record.phones]}"
                        )
                    elif change == "2":
                        mail = input(Style.BRIGHT + Fore.CYAN + "Enter new email: ")
                        record.create_email(record=record, user_email=mail)
                        print(
                            Back.BLUE
                            + Fore.RED
                            + f"In contact {name} change or append email "
                            f"{record.email.value}"
                        )
                    elif change == "3":
                        birthday = input(Style.BRIGHT + Fore.CYAN + "Enter new date: ")
                        record.create_birthday(record=record, user_birthday=birthday)
                        print(
                            Style.BRIGHT
                            + Back.BLUE
                            + Fore.RED
                            + f"In contact {name} change or append date birthday"
                            f"{record.birthday.value}"
                        )
                    elif change == "4":
                        new_name = input(Style.BRIGHT + Fore.CYAN + "Enter new name: ")
                        record.name = Name(new_name)
                        update_name_data[name] = new_name
                        print(
                            "\033[3m\033[33m\033[41m{}\033[0m".format(
                                "Contact name changed to:"
                            ),
                            Style.BRIGHT + Fore.LIGHTGREEN_EX + record.name.value,
                        )
                    elif change == "5":
                        num = input(Style.BRIGHT + Fore.CYAN + "Enter number: ")
                        record.create_phone(record=record, user_input=num, update=True)
                        print(
                            Style.BRIGHT
                            + Back.BLUE
                            + Fore.RED
                            + f"In contact {name} update "
                            f"{[phone.value for phone in record.phones]}"
                        )
                    elif change == "6":
                        new_address = input(
                            Style.BRIGHT + Fore.CYAN + "Enter new address: "
                        )
                        record.home_address_create(
                            record=record, user_address=new_address
                        )
                        print(
                            Style.BRIGHT
                            + Back.BLUE
                            + Fore.RED
                            + f"In contact {name} change or append home address"
                            f" {record.home_address.value}"
                        )
                    else:
                        print(Style.BRIGHT + Fore.RED + f"{change} invalid choice")
                        return
            for name, new_name in update_name_data.items():
                self.address_book.data[new_name] = self.address_book.data.pop(name)
            if flag:
                self.address_book.save_contacts()
            else:
                print("\033[4m\033[31m\033[45m{}\033[0m".format("User not fount"))

    def remove_contacts(self):
        """Delete contact from address book"""
        remove_commands = PrettyTable()
        remove_commands.field_names = ["Command entry", "Command value"]
        remove_commands.add_row(["del", "Delete one selected contact"])
        remove_commands.add_row(["del all", "Delete all address book contacts"])
        print("\033[1m\033[31m{}\033[0m".format(remove_commands))
        remove_date = input(Style.BRIGHT + Fore.YELLOW + "Enter your choice: ")
        if remove_date == "del":
            remove_user = input(
                Style.BRIGHT + Fore.YELLOW + "Enter the name of the contact "
                "to be deleted: "
            )
            self.address_book.data.pop(remove_user)
            print(Style.BRIGHT + Fore.RED + f"Contact {remove_user} deleted.")
            self.address_book.save_contacts()
        elif remove_date == "del all":
            print(
                Style.BRIGHT + Fore.RED + f"Are you sure you want to "
                f"clear the Address Book?"
            )
            question = input(Style.BRIGHT + Fore.RED + "Y or N: ").lower().strip()
            if question == "n":
                return
            elif question == "y":
                self.address_book.data.clear()
            self.address_book.save_contacts()
        else:
            print(Style.BRIGHT + Fore.RED + f"Invalid command")

    def get_back(self):
        """Back to main menu"""
        pass


class TableOutput(ABC):
    @abstractmethod
    def create_header(self):
        pass

    @abstractmethod
    def convert_data_to_table(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


class AddressBookDataOutput(TableOutput):
    def create_header(self, column_names: list):
        self.table = PrettyTable(column_names)
        self.table.hrules = ALL

    def convert_data_to_table(self, data):
        for i in data.values():
            phones = "\n".join(map(str, i.phones))
            self.table.add_row([i.name, phones, i.email, i.birthday, i.home_address])

    def __str__(self):
        return f"{self.table}"


class HelpOutput(TableOutput):
    def create_header(self, welcome_string):
        self.table = [welcome_string]

    def convert_data_to_table(self, commands):
        for k, v in commands.items():
            self.table.append(f"|{k} - {v.__doc__}")

    def __str__(self):
        return "\n".join(self.table)


# ------------------------------------------------ADAPTER-------------------------------------------------------

help = (
    "|You can use following commands:\n"
    "|add - Add new contact\n"
    "|find - Find contact in Address Book\n"
    "|show all - Shows the entire Address Book\n"
    "|get bith - Show birthdays\n"
    "|change - Change contact\n"
    "|del - Delete contact from address book\n"
    "|back - Closing the sublayer\n"
)

commands = {
    "add": CommandsHandler().add_contacts,
    "help": CommandsHandler().get_help,
    "find": CommandsHandler().find_contacts,
    "show all": CommandsHandler().show_all,
    "get bith": CommandsHandler().birthday_contacts,
    "change": CommandsHandler().change_contacts,
    "del": CommandsHandler().remove_contacts,
    "back": CommandsHandler().get_back,
}

CONFIG = {"help": help, "commands": commands}


if __name__ == "__main__":
    CommandsHandler().get_help()
    CommandsHandler().show_all()
