from abc import ABC, abstractmethod
from AddressBook.AddressBook import AddressBook
from typing import Optional


class AddressContainerInterface(ABC):
    """
    An abstract base class that defines the interface for an address container,
    which can store, retrieve, update, and delete addresses, as well as handle
    file operations and birthday notifications.
    """

    @abstractmethod
    def set_filepath(self, filepath: str):
        """
        Set the file path for the database.

        :param str filepath: PATH to the file
        """
        pass

    @abstractmethod
    def open(self):
        """
        Open the database file for reading or writing.
        If the file doesn't exist, it creates a new one.
        """
        pass

    @abstractmethod
    def close(self):
        """
        Close the currently opened database file.
        Ensure that all resources, such as file handlers, are properly released.
        """
        pass

    @abstractmethod
    def save(self):
        """
        Save any changes made to the database.
        This function should write the current state of the address book to the file.
        """
        pass

    @abstractmethod
    def search(self, field: str, search_string: str) -> dict[int, AddressBook]:
        """
        Search for a string in a specific field (e.g., name, phone, email).
        Return a dictionary containing all matching addresses.

        :param str field: The field to search within.
        :param str search_string: The search term to look for.
        :return: A dictionary where keys are IDs and values are matching addresses.
        :rtype: dict[int, AddressBook]
        """
        pass

    @abstractmethod
    def delete(self, id_: int) -> int | None:
        """
        Delete an address by its ID.

        :param int id_: The ID of the address to delete.
        :return: The ID of the deleted address if successful, or None if the ID doesn't exist.
        :rtype: int or None:
        """
        pass

    @abstractmethod
    def update(self, id_: int, **kwargs) -> int:
        """
        Update an existing address by its ID.

        :param int id_: The ID of the address to update.
        :param kwargs: Key-value pairs of fields to update in the address.
        :return: The ID of the updated address if successful.
        :rtype: int
        :raise KeyError: If the address with the specified ID is not found.
        """
        pass

    @abstractmethod
    def add_address(self, address: AddressBook) -> int:
        """
        Add a new address to the address book.

        :param AddressBook address: The address object to add (can be a dictionary or AddressBook instance).
        :return: The ID of the newly added address.
        :rtype: int
        """
        pass

    @abstractmethod
    def get_all(self) -> dict[int, AddressBook]:
        """
        Retrieve all addresses stored in the address book.

        :return: A dictionary where keys are IDs and values are address objects.
        :rtype: dict[int, AddressBook]
        """
        pass

    @abstractmethod
    def get(self, id_: int) -> AddressBook or None:
        """
        Retrieve a specific address by its ID.

        :param int id_: The ID of the address to retrieve.
        :return: The address if found, or None if the ID does not exist.
        :rtype: AddressBook, None
        """
        pass

    @abstractmethod
    def get_todays_birthdays(self) -> dict[int, AddressBook]:
        """
        Retrieve addresses of persons who have their birthday today.

        :return: A dictionary where keys are IDs and values are addresses of people whose birthday is today.
        :rtype: dict[int, AddressBook]
        """
        pass
