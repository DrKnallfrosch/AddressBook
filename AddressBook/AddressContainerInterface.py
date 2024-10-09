from abc import ABC, abstractmethod
from AddressBook import AddressBook
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

        Args:
            filepath (str): The path to the file where the addresses will be stored.
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
    def search(self, field: str, search_string: str) -> dict:
        """
        Search for a string in a specific field (e.g., name, phone, email).
        Return a dictionary containing all matching addresses.

        Args:
            field (str): The field to search within (e.g., "name", "email").
            search_string (str): The search term to look for.

        Returns:
            dict: A dictionary where keys are IDs and values are matching addresses.
        """
        pass

    @abstractmethod
    def delete(self, id_: int) -> int | None:
        """
        Delete an address by its ID.

        Args:
            id_ (int): The ID of the address to delete.

        Returns:
            int | None: The ID of the deleted address if successful, or None if the ID doesn't exist.
        """
        pass

    @abstractmethod
    def update(self, id_: int, **kwargs) -> int:
        """
        Update an existing address by its ID.

        Args:
            id_ (int): The ID of the address to update.
            **kwargs: Key-value pairs of fields to update in the address.

        Returns:
            int: The ID of the updated address if successful.

        Raises:
            KeyError: If the address with the specified ID is not found.
        """
        pass

    @abstractmethod
    def add_address(self, address) -> int:
        """
        Add a new address to the address book.

        Args:
            address: The address object to add (can be a dictionary or AddressBook instance).

        Returns:
            int: The ID of the newly added address.
        """
        pass

    @abstractmethod
    def get_all(self) -> dict:
        """
        Retrieve all addresses stored in the address book.

        Returns:
            dict: A dictionary where keys are IDs and values are address objects.
        """
        pass

    @abstractmethod
    def get(self, id_: int) -> AddressBook | None:
        """
        Retrieve a specific address by its ID.

        Args:
            id_ (int): The ID of the address to retrieve.

        Returns:
            AddressBook | None: The address if found, or None if the ID does not exist.
        """
        pass

    @abstractmethod
    def get_todays_birthdays(self) -> dict:
        """
        Retrieve addresses of persons who have their birthday today.

        Returns:
            dict: A dictionary where keys are IDs and values are addresses of people whose birthday is today.
        """
        pass
