from collections import UserDict
from datetime import datetime, date, timedelta
import pickle


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def find_phone(self, search_phone):
        for phone in self.phones:
            if phone.value == search_phone:
                return phone
        return None

    def remove_phone(self, phone_to_remove):
        phone = self.find_phone(phone_to_remove)
        if phone is None:
            return
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        phone = self.find_phone(old_phone)
        if phone is None:
            raise ValueError
        Phone(new_phone)
        self.add_phone(new_phone)
        self.remove_phone(old_phone)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, record_name):
        return self.data.get(record_name)

    def delete(self, record_to_delete):
        del self.data[record_to_delete]

    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = date.today()
        for key, value in self.data.items():
            if value.birthday is None:
                continue
            birthday_date = datetime.strptime(value.birthday.value, "%d.%m.%Y").date()
            birthday_this_year = birthday_date.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)
            if 0 <= (birthday_this_year - today).days <= days:
                congratulation_date = adjust_for_weekend(birthday_this_year)
                congratulation_date_str = date_to_string(congratulation_date)
                upcoming_birthdays.append(
                    {"name": key, "birthday": congratulation_date_str}
                )
        return upcoming_birthdays

    def __str__(self):
        return "\n".join(record.__str__() for record in self.data.values())


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def date_to_string(date):
    return date.strftime("%d.%m.%Y")


def find_next_weekday(start_date, weekday):
    days_ahead = weekday - start_date.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return start_date + timedelta(days=days_ahead)


def adjust_for_weekend(birthday):
    if birthday.weekday() >= 5:
        return find_next_weekday(birthday, 0)
    return birthday


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except ValueError:
            return "Give me name and phone please."

        except KeyError:
            return "This name does not exist."

        except IndexError:
            return "Enter user name."

    return inner


@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book):
    name, phone_old, phone_new = args
    find_record = book.find(name)
    if find_record is None:
        return "Record is not found"
    find_record.edit_phone(phone_old, phone_new)
    return "Contact updated."


@input_error
def show_phone(args, book):
    name = args[0]
    find_record = book.find(name)
    if find_record is None:
        return "Record is not found"
    if find_record.phones == []:
        return "No phones for this contact"
    result = ""
    for phone in find_record.phones:
        result += f"{phone}\n"
    return result


def show_all(book):
    if not book.data:
        return "No contacts"
    result = ""
    for record in book.data.values():
        result += f"{str(record)}\n"
    return result


@input_error
def add_birthday(args, book):
    name, birthday = args
    find_record = book.find(name)
    if find_record is None:
        return "No record"
    find_record.add_birthday(birthday)
    return "Birthday is added"


@input_error
def show_birthday(args, book):
    name = args[0]
    find_record = book.find(name)
    if find_record is None:
        return "Name is not found"
    if find_record.birthday is None:
        return "No birthday for this contact"
    return find_record.birthday.value


@input_error
def birthdays(args, book):
    congratulations = book.get_upcoming_birthdays()
    if congratulations == []:
        return "No upcoming birthdays"
    return congratulations

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        if user_input.strip() == "":
            print("Enter a command:")
            continue
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()