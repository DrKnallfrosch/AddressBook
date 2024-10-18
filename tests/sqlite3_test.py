import os
import unittest
from AddressBook.Address import Address
from AddressBook.AddressDatabaseSQL import AddressDatabaseSQL


class TestAddressSQLite(unittest.TestCase):

    def setUp(self):
        self.db = AddressDatabaseSQL()
        self.db.set_filepath('test.db')
        self.db.open()

    def tearDown(self):
        self.db.close()
        os.remove(self.db.filepath)

    def test_set_filepath_invalid(self):
        with self.assertRaises(ValueError) as context:
            self.db.set_filepath('Invalid_format.')
        self.assertEqual(str(context.exception), "Invalid File Format. Required: .db Database file")

    def test_add_address(self):
        address = Address(firstname='John', lastname='Doe', email='123@gmail.com')
        new_id = self.db.add_address(address)
        self.assertEqual(new_id, 1)

    def test_is_duplicate(self):
        address = Address(firstname='John', lastname='Doe', email='123@gmail.com')
        self.db.add_address(address)
        self.assertTrue(self.db.is_duplicate(address))

    def test_get_all(self):
        address = Address(firstname='John', lastname='Doe', email='123@gmail.com')
        self.db.add_address(address)
        all_addresses = self.db.get_all()
        self.assertEqual(len(all_addresses), 1)
        self.assertIn(1, all_addresses)

    def test_get(self):
        address = Address(firstname='John', lastname='Doe', email='123@gmail.com')
        new_id = self.db.add_address(address)
        fetched_address = self.db.get(new_id)
        self.assertEqual(fetched_address.firstname, 'John')

    def test_search(self):
        address = Address(firstname='John', lastname='Doe', email='123@gmail.com')
        self.db.add_address(address)
        results = self.db.search('John', 'firstname')
        self.assertEqual(len(results), 1)
        self.assertIn(1, results)

    def test_delete(self):
        address = Address(firstname='John', lastname='Doe', email='123@gmail.com')
        new_id = self.db.add_address(address)
        self.db.delete(new_id)
        self.assertIsNone(self.db.get(new_id))

    def test_update(self):
        address = Address(firstname='John', lastname='Doe', email='123@gmail.com')
        new_id = self.db.add_address(address)
        self.db.update(new_id, firstname='Jane')
        updated_address = self.db.get(new_id)
        self.assertEqual(updated_address.firstname, 'Jane')


if __name__ == '__main__':
    unittest.main()