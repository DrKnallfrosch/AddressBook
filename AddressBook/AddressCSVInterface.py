import AddressContainerInterface
import AddressBook
import csv


class AddressCSVInterface(AddressContainerInterface):

    def set_filepath(self, filepath: str):
        pass

    def read(self):
        pass

    def save(self):
        pass

    def search(self, search_string: str) -> dict:
        pass

    def add_address(self, address) -> int:
        pass

    def delete_address(self, address_id: int) -> int:
        pass

    def update_address(self, address_id: int, **kwargs) -> int:
        pass

    def get_all(self) -> dict:
        pass

    def get_address(self, address_id: int) -> AddressBook:
        pass

    def get_bd_today(self) -> dict:
        pass
