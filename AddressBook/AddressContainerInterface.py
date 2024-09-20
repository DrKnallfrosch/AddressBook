from abc import ABC, abstractmethod
from AddressBook import AddressBook

 
class AddressContainerInterface(ABC):

    @abstractmethod
    def set_filepath(self, filepath: str):
        pass

    @abstractmethod
    def open(self):
        """Open the database or create a new one"""
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def search(self, field: str, search_string: str) -> dict:
        """Search for a string in any field. Return a dictionary with the found addresses. Keys are the ids and
        values the addresses"""
        pass

    @abstractmethod
    def delete(self, id_: int) -> int | None:
        """Delete an address by id. Return the number of deleted address if successful"""
        pass

    @abstractmethod
    def update(self, id_: int, **kwargs) -> int:
        """Update an address by id. Return the ID of the updated addresses if successful
        or raises an KeyError"""
        pass

    @abstractmethod
    def add_address(self, address) -> int:
        """Add an address. Return the id of the added address"""
        pass

    @abstractmethod
    def get_all(self) -> dict:
        """Return a dictionary with all addresses"""
        pass

    @abstractmethod
    def get(self, id_: int) -> AddressBook | None:
        """Return an address by id"""
        pass

    @abstractmethod
    def get_todays_birthdays(self) -> dict:
        """Return a dictionary with the addresses of the persons who have birthday today"""
        pass
