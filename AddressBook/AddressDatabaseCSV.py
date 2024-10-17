import csv
from AddressBook.AddressBook import AddressBook
from AddressBook.AddressContainerInterface import AddressContainerInterface
from typing import Optional, Dict
from datetime import date
from pydantic import ValidationError


class AddressDatabaseCSV(AddressContainerInterface):
    """
    A concrete implementation of AddressContainerInterface for managing address data stored in a CSV file.

    This class provides methods to load, search, add, update, delete, and save address book entries.

    :ivar filepath: Path to the CSV file that stores address book data.
    :ivar addresses: A dictionary of address entries with IDs as keys.
    """

    def __init__(self):
        """
        Initializes the AddressDatabaseCSV with an empty address dictionary and no CSV file path.
        """
        self.filepath: str or None = None
        self.addresses: Dict[int, AddressBook] = {}

    def set_filepath(self, filepath: str):
        """
        Sets the file path for the CSV file that contains the address data.

        :param str filepath: The path to the CSV file.
        """
        self.filepath = filepath

    def open(self):
        """
        Opens the CSV file at the specified file path and loads its contents into the internal address dictionary.

        Each row in the CSV file represents an address entry. If the file is not found, the dictionary remains empty.

        :raises FileNotFoundError: If the specified CSV file does not exist.
        """
        try:
            with open(self.filepath, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for idx, row in enumerate(reader, start=1):
                    try:
                        # Ensure no leading/trailing spaces in the emails
                        row['email'] = row['email'].strip() if row['email'] else ''
                        address = AddressBook(
                            firstname=row['firstname'],
                            lastname=row['lastname'],
                            street=row.get('street'),
                            number=row.get('number'),
                            postal_code=int(row['postal_code']) if row['postal_code'] else None,
                            place=row.get('place'),
                            birthdate=row.get('birthdate'),
                            phone=row.get('phone'),
                            email=row['email']
                        )
                        self.addresses[idx] = address
                    except ValidationError as e:
                        print(f"Error loading address at row {idx}: {e}")
                        continue
        except FileNotFoundError:
            print(f"File {self.filepath} not found. Initializing empty dictionary.")
            self.addresses = {}

    def save(self):
        """
        Saves the current address entries back into the CSV file, overwriting the previous contents.
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

    def close(self):
        """
        Clears the internal dictionary of addresses, releasing any memory or resources.
        """
        self.addresses.clear()

    def search(self, field: str, search_string: str) -> Dict[int, AddressBook]:
        """
        Searches for a string in the specified field of the address entries.

        :param str field: The field to search within (e.g., "firstname", "lastname", "email").
        :param str search_string: The string to search for in the field.
        :return: A dictionary of matching address entries.
        :rtype: Dict[int, AddressBook]

        :raises ValueError: If the specified field does not exist in AddressBook.
        """
        result = {}
        for id_, address in self.addresses.items():
            if getattr(address, field, "").lower() == search_string.lower():
                result[id_] = address
        return result

    def delete(self, id_: int) -> Optional[int]:
        """
        Deletes the address entry with the specified ID.

        :param int id_: The ID of the address entry to delete.
        :return: The ID of the deleted entry, or None if the ID was not found.
        :rtype: int or None
        """
        return self.addresses.pop(id_, None)

    def update(self, id_: int, **kwargs) -> int:
        """
        Updates the address entry with the given ID using the provided keyword arguments.

        :param id_: The ID of the address entry to update.
        :type id_: int
        :param kwargs: The fields to update in the address entry (e.g., firstname, email).
        :return: The ID of the updated entry.
        :rtype: int
        :raises KeyError: If the ID does not exist in the address book.
        """
        if id_ in self.addresses:
            for key, value in kwargs.items():
                if hasattr(self.addresses[id_], key):
                    setattr(self.addresses[id_], key, value)
            return id_
        else:
            raise KeyError(f"No address found with ID {id_}")

    def add_address(self, address: AddressBook) -> int:
        """
        Adds a new address entry to the address book.

        :param address: The AddressBook instance to add.
        :type address: AddressBook
        :return: The new ID of the added address entry, or -1 if the entry is a duplicate.
        :rtype: int
        """
        if self.is_duplicate(address):
            return -1
        new_id = max(self.addresses.keys(), default=0) + 1
        self.addresses[new_id] = address
        return new_id

    def get_all(self) -> Dict[int, AddressBook]:
        """
        Returns all address entries as a dictionary.

        :return: A dictionary of all address entries, keyed by ID.
        :rtype: Dict[int, AddressBook]
        """
        return self.addresses

    def get(self, id_: int) -> Optional[AddressBook]:
        """
        Retrieves the address entry with the specified ID.

        :param id_: The ID of the address entry to retrieve.
        :type id_: int
        :return: The AddressBook object, or None if the ID was not found.
        :rtype: AddressBook, optional
        """
        return self.addresses.get(id_)

    def get_todays_birthdays(self) -> Dict[int, AddressBook]:
        """
        Returns all address entries where today is the person's birthday.

        :return: A dictionary of address entries with today's birthday, keyed by their IDs.
        :rtype: Dict[int, AddressBook]
        """
        result = {}
        today = date.today().strftime("%m-%d")
        for id_, address in self.addresses.items():
            if address.birthdate and address.birthdate[5:] == today:
                result[id_] = address
        return result

    def is_duplicate(self, address: AddressBook) -> bool:
        """
        Checks if an address entry is a duplicate by comparing its firstname, lastname, and email with existing entries.

        :param address: The AddressBook instance to check for duplicates.
        :return: True if the address entry is a duplicate, otherwise False.
        :rtype: bool
        """
        for existing in self.addresses.values():
            if (existing.firstname == address.firstname and
                    existing.lastname == address.lastname and
                    existing.email == address.email):
                return True
        return False
