from helpers.address_book import AddressBook, Record

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError as e:
            return f"Contact with the name {e} doesn't exists. Use 'add [name] [new_phone]' to add."
        except IndexError:
            return "Invalid command format. Use 'phone [name]' to get contact number."
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

    return inner

@input_error
def add_contact(args, book):
    if len(args) == 2:
        name, phone = args
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."
    else:
        raise ValueError("Invalid command format. Use '[name] [phone]' as command arguments.")

@input_error
def change_contact(args, book):
    if len(args) == 2:
        name, new_phone = args
        record = book.find(name)
        if record:
            record.edit_phone(record.phones[0].value, new_phone)
            return "Contact updated."
        else:
           raise KeyError(name)
    else:
        raise ValueError("Invalid command format. Use '[name] [phone]' as command arguments.")

@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        return record.phones[0].value
    else:
        raise KeyError(name)

@input_error
def show_all(book):
    if book.data.values():
        for record in book.data.values():
            print(record)
    else:
        print("No contacts available.")

@input_error
def add_birthday(args, book):
    if len(args) == 2:
        name, birthday = args
        record = book.find(name)
        if record:
            record.add_birthday(birthday)
            return "Birthday added."
        else:
            raise KeyError(name)
    else:
        raise ValueError("Invalid command format. Use '[name] [date]' as command arguments.")

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return record.birthday.value
    else:
        raise KeyError(name)

def birthdays(book):
    birthdays = book.get_birthdays_per_week()
    if birthdays:
        return "\n".join([f"{name}: {', '.join(birthday)}" for name, birthday in birthdays.items()])
    else:
        return "No upcoming birthdays."

def main():
    try:
        book = AddressBook()
        book.load_from_file("address_book.dat")
        print("Welcome to the assistant bot!")
        while True:
            user_input = input("Enter a command: ")
            command, *args = parse_input(user_input)

            if command in ["close", "exit"]:
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
                show_all(book)
            elif command == "add-birthday":
                print(add_birthday(args, book))
            elif command == "show-birthday":
                print(show_birthday(args, book))
            elif command == "birthdays":
                print(birthdays(book))
            else:
                print("Invalid command.")
    finally:
        book.save_to_file("address_book.dat")

if __name__ == "__main__":
    main()