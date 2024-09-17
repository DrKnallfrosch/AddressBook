import csv
import logging
from AddressBook import AddressBook
from AddressContainerInterface import AddressContainerInterface
from typing import Optional, Dict
from datetime import datetime
from pydantic import ValidationError

logging.basicConfig(level=logging.INFO)


class AddressDatabaseCSV(AddressContainerInterface):

    def __init__(self):
        # Initialize with no filepath and an empty dictionary for addresses
        self.filepath = None
        self.addresses: Dict[int, AddressBook] = {}

    def set_filepath(self, filepath: str):
        """Set the CSV file path."""
        self.filepath = filepath

    def open(self):
        """Open the CSV file and load data into the internal dictionary."""
        try:
            with open(self.filepath, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                print("CSV Headers:", reader.fieldnames)  # Debug header
                for idx, row in enumerate(reader, start=1):
                    try:
                        # Create an AddressBook object from each row
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
                        # Use a generated ID if 'id' is missing in the CSV
                        self.addresses[idx] = address
                    except ValidationError as e:
                        # Log validation errors for addresses
                        print(f"Error loading address at row {idx}: {e}")
        except FileNotFoundError:
            # If the file does not exist, initialize with an empty dictionary
            self.addresses = {}

    def close(self):
        """Clear the internal dictionary to release resources."""
        self.addresses.clear()

    def save(self):
        """Save the current dictionary data back to the CSV file."""
        with open(self.filepath, mode='w', newline='', encoding='utf-8') as file:
            # Define the fieldnames for the CSV file
            fieldnames = ['firstname', 'lastname', 'street', 'number', 'postal_code', 'place', 'birthdate',
                          'phone', 'email']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for id_, address in self.addresses.items():
                # Write each address to the CSV file
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

    def search(self, search_string: str) -> Dict[int, AddressBook]:
        """Search for a string in any field and return matching addresses."""
        result = {}
        search_string_lower = search_string.lower()
        for id_, address in self.addresses.items():
            # Check if the search string is found in any of the address fields
            if (search_string_lower in address.firstname.lower() or
                    search_string_lower in address.lastname.lower() or
                    (address.street and search_string_lower in address.street.lower()) or
                    (address.number and search_string_lower in address.number.lower()) or
                    (address.place and search_string_lower in address.place.lower()) or
                    (address.email and search_string_lower in address.email.lower())):
                result[id_] = address
        return result

    def delete(self, id_: int) -> Optional[int]:
        """Delete an address by id. Return the id of the deleted address if successful."""
        if id_ in self.addresses:
            del self.addresses[id_]
            self.save()  # Save changes to the CSV file
            return id_
        return None

    def update(self, id_: int, **kwargs) -> int:
        """Update an address by id. Return the ID of the updated address if successful, or raise a KeyError."""
        if id_ not in self.addresses:
            raise KeyError(f"Address with id {id_} not found")

        # Update address fields if they exist in kwargs
        address = self.addresses[id_]
        for key, value in kwargs.items():
            if hasattr(address, key):
                setattr(address, key, value)

        self.save()  # Save changes to the CSV file
        return id_

    def add_address(self, address: AddressBook) -> int:
        """Add a new address entry if it does not already exist."""
        if self.is_duplicate(address):
            logging.info("This address book entry already exists.")
            return -1

        new_id = max(self.addresses.keys(), default=0) + 1
        self.addresses[new_id] = address
        self.save()  # Save changes to the CSV file
        return new_id

    def get_all(self) -> Dict[int, AddressBook]:
        """Return a dictionary with all addresses."""
        return self.addresses

    def get(self, id_: int) -> Optional[AddressBook]:
        """Return an address by id."""
        return self.addresses.get(id_)

    def get_todays_birthdays(self) -> Dict[int, AddressBook]:
        """Return a dictionary with the addresses of persons who have a birthday today."""
        today = datetime.today()
        today_month_day = (today.month, today.day)

        # Collect addresses whose birthdate matches today's month and day
        birthdays_today = {}
        for id_, address in self.addresses.items():
            if address.birthdate:
                try:
                    birthdate = datetime.strptime(address.birthdate, '%Y-%m-%d')
                    if (birthdate.month, birthdate.day) == today_month_day:
                        birthdays_today[id_] = address
                except ValueError:
                    # Handle the case where the birthdate is not in the expected format
                    print(f"Error parsing birthdate for address with ID {id_}")

        return birthdays_today

    def is_duplicate(self, address: AddressBook) -> bool:
        """Check if an address book entry already exists."""
        for existing_address in self.addresses.values():
            # Check if first name, last name, and email match
            if (existing_address.firstname == address.firstname and
                    existing_address.lastname == address.lastname and
                    existing_address.email == address.email):
                return True  # Duplicate found
        return False


if __name__ == '__main__':
    a = AddressDatabaseCSV()
    a.set_filepath(r"C:\Users\schue\Documents\Programmierung\Projects\Python\AddressBook\AddressBook\CSV\address.csv")
    print(a.filepath)
    a.open()
    a.save()
    print(a.get_all())
    print(a.search("Tim"))
    #a.delete(2)
    print(a.get(1))
    a.update(2, birthdate="2005-06-26")
    print(a.get(2))
    b = AddressBook(firstname="Domink", lastname="Hase")
    a.add_address(b)
    print(a.get(3))
    a.update(3, birthdate="2006-09-16")
    print(a.get_todays_birthdays())
