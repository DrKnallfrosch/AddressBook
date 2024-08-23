from abc import ABC, abstractmethod
from AddressBook import AddressBook

 
class AddressContainerInterface(ABC):

    @abstractmethod
    def set_filepath(self, filepath: str):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def get_all(self) -> dict:
        pass

    @abstractmethod
    def get_address(self, address_id: int) -> AddressBook:
        pass

    @abstractmethod
    def get_bd_today(self) -> dict:
        pass

    @abstractmethod
    def search(self, search_string: str) -> dict:
        pass

    @abstractmethod
    def add_address(self, address) -> int:
        pass

    @abstractmethod
    def delete_address(self, address_id: int) -> int:
        pass

    @abstractmethod
    def update_address(self, address_id: int, **kwargs) -> int:
        pass
