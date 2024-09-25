import csv
import logging
from AddressBook.AddressBook import AddressBook
from AddressBook.AddressContainerInterface import AddressContainerInterface
from typing import Optional, Dict
from datetime import datetime
from pydantic import ValidationError

logging.basicConfig(level=logging.INFO)


class AddressDatabaseCSV(AddressContainerInterface):
    """
    A concrete implementation of AddressContainerInterface for handling address data stored in a CSV file.
    Provides functionalities to load, search, add, update, delete, and save address book entries.
    """

    def __init__(self):
        """
        Initialize the AddressDatabaseCSV object with no filepath and an empty address dictionary.
        """
        self.filepath = None
        self.addresses: Dict[int, AddressBook] = {}

    def set_filepath(self, filepath: str):
        """
        Set the file path for the CSV file that contains the address data.

        Args:
            filepath (str): The path to the CSV file.
        """
        self.filepath = filepath

    def open(self):
        """
        Open the CSV file and load data into the internal dictionary. Each row in the CSV corresponds to an address.
        If the file is not found, it initializes an empty dictionary.
        """
        try:
            with open(self.filepath, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                print("CSV Headers:", reader.fieldnames)  # Debug header
                for idx, row in enumerate(reader, start=1):
                    try:
                        address = AddressBook(
                            firstname=row['firstname'],
                            lastname=row['lastname'],
                            street=row['street'] if row['street'] else None,
                            number=row['number'] if row['number'] else None,
                            postal_code=int(row['postal_code']) if row['postal_code'] else None,
                            place=row['place'] if row['place'] else None,
                            birthdate=row['birthdate'] if row['birthdate'] else None,
                            phone=row['phone'] if row['phone'] else None,
                            email=row['email'] if row['email'] else None
                        )
                        self.addresses[idx] = address  # Store the address with an ID.
                    except ValidationError as e:
                        print(f"Error loading address at row {idx}: {e}")
        except FileNotFoundError:
            self.addresses = {}  # Initialize an empty dictionary if the file doesn't exist.

    def close(self):
        """
        Clear the internal dictionary of addresses, releasing any memory or resources.
        """
        self.addresses.clear()

    def save(self):
        """
        Save the current address data to the CSV file, overwriting any existing file contents.
        Writes all addresses stored in the dictionary back into the CSV file.
        """
        with open(self.filepath, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['firstname', 'lastname', 'street', 'number', 'postal_code', 'place', 'birthdate', 'phone',
                          'email']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for id_, address in self.addresses.items():
                writer.writerow({
                    'firstname': address.firstname,
                    'lastname': address.lastname,
                    'street': address.street,
                    'number': address.number,
                    'postal_code': address.postal_code,
                    'place': address.place,
                    'birthdate': address.birthdate,
                    'phone': address.phone,
                    'email': address.email
                })

    def search(self, field: str, search_string: str) -> Dict[int, AddressBook]:
        """
        Search for a string in the specified field of the address entries.

        Args:
            field (str): The field to search within (e.g., "firstname", "lastname", "email").
            search_string (str): The string to search for in the specified field.

        Returns:
            dict: A dictionary containing matching address entries with IDs as keys.
        """
        result = {}
        columns = ['firstname', 'lastname', 'street', 'number', 'postal_code', 'place', 'birthdate', 'phone', 'email']
        check = any(field in x for x in columns)
        if not check:
            raise ValueError(f"Invalid field: {field}")
        search_string_lower = search_string.lower()
        for id_, address in self.addresses.items():
            match field:
                case 'firstname':
                    if search_string_lower in address.firstname.lower():
                        result[id_] = address
                case 'lastname':
                    if search_string_lower in address.lastname.lower():
                        result[id_] = address
                case 'street':
                    if search_string_lower in address.street.lower():
                        result[id_] = address
                case 'number':
                    if search_string_lower in address.number.lower():
                        result[id_] = address
                case 'postal_code':
                    if search_string_lower in str(address.postal_code).lower():
                        result[id_] = address
                case 'place':
                    if search_string_lower in address.place.lower():
                        result[id_] = address
                case 'birthdate':
                    if search_string_lower in address.birthdate.lower():
                        result[id_] = address
                case 'phone':
                    if search_string_lower in address.phone.lower():
                        result[id_] = address
                case 'email':
                    if search_string_lower in address.email.lower():
                        result[id_] = address
        return result

    def delete(self, id_: int) -> Optional[int]:
        """
        Delete an address by its ID.

        Args:
            id_ (int): The ID of the address to delete.

        Returns:
            Optional[int]: The ID of the deleted address if found and removed, otherwise None.
        """
        if id_ in self.addresses:
            del self.addresses[id_]
            self.save()  # Save changes after deletion.
            return id_
        return None

    def update(self, id_: int, **kwargs) -> int:
        """
        Update fields of an address by its ID. Raises KeyError if the ID is not found.

        Args:
            id_ (int): The ID of the address to update.
            **kwargs: Field names and their updated values (e.g., firstname="John").

        Returns:
            int: The ID of the updated address.

        Raises:
            KeyError: If the address with the given ID is not found.
        """
        if id_ not in self.addresses:
            raise KeyError(f"Address with id {id_} not found")

        address = self.addresses[id_]
        for key, value in kwargs.items():
            if hasattr(address, key):
                setattr(address, key, value)

        self.save()  # Save changes after updating.
        return id_

    def add_address(self, address: AddressBook) -> int:
        """
        Add a new address to the address book, ensuring no duplicates are added.

        Args:
            address (AddressBook): The address to add.

        Returns:
            int: The ID of the newly added address, or -1 if it already exists.
        """
        if self.is_duplicate(address):
            logging.info("This address book entry already exists.")
            return -1

        new_id = max(self.addresses.keys(), default=0) + 1
        self.addresses[new_id] = address
        self.save()  # Save changes after adding the new address.
        return new_id

    def get_all(self) -> Dict[int, AddressBook]:
        """
        Return all address entries as a dictionary.

        Returns:
            dict: A dictionary where keys are IDs and values are AddressBook objects.
        """
        return self.addresses

    def get(self, id_: int) -> Optional[AddressBook]:
        """
        Retrieve an address by its ID.

        Args:
            id_ (int): The ID of the address to retrieve.

        Returns:
            Optional[AddressBook]: The address if found, otherwise None.
        """
        return self.addresses.get(id_)

    def get_todays_birthdays(self) -> Dict[int, AddressBook]:
        """
        Get all addresses of persons who have their birthday today.

        Returns:
            dict: A dictionary where keys are IDs and values are AddressBook objects of people whose birthday is today.
        """
        today = datetime.today()
        today_month_day = (today.month, today.day)

        birthdays_today = {}
        for id_, address in self.addresses.items():
            if address.birthdate:
                try:
                    birthdate = datetime.strptime(address.birthdate, '%Y-%m-%d')
                    if (birthdate.month, birthdate.day) == today_month_day:
                        birthdays_today[id_] = address
                except ValueError:
                    print(f"Error parsing birthdate for address with ID {id_}")

        return birthdays_today

    def is_duplicate(self, address: AddressBook) -> bool:
        """
        Check if an address is a duplicate based on first name, last name, and email.

        Args:
            address (AddressBook): The address to check for duplicates.

        Returns:
            bool: True if a duplicate is found, otherwise False.
        """
        for existing_address in self.addresses.values():
            if (existing_address.firstname == address.firstname and
                    existing_address.lastname == address.lastname and
                    existing_address.email == address.email):
                return True
        return False


if __name__ == '__main__':
    a = AddressDatabaseCSV()
    a.set_filepath(r"C:\Users\schue\Documents\Programmierung\Projects\Python\AddressBook\AddressPack\CSV\address.csv")
    print(a.filepath)
    a.open()
    a.save()
    print(a.get_all())
    print(a.search("firstname", "Tim"))
    #  a.delete(2)
    print(a.get(1))
    a.update(2, birthdate="2005-06-26")
    print(a.get(2))
    b = AddressBook(firstname="Domink", lastname="Hase")
    a.add_address(b)
    print(a.get(3))
    a.update(3, birthdate="2006-09-16")
    print(a.get_todays_birthdays())
