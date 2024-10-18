import unittest
from unittest.mock import patch, mock_open
from AddressBook.Address import Address
from AddressBook.AddressDatabaseCSV import AddressDatabaseCSV


class TestAddressDatabaseCSV(unittest.TestCase):

    def setUp(self):
        self.db = AddressDatabaseCSV()

    @patch('builtins.open', new_callable=mock_open,
           read_data='id,firstname,lastname,street,number,postal_code,place,birthdate,phone,email\n'
                     '1,John,Doe,,,12345,,1990-01-01,123@gmail.com\n'
                     '2,Jane,Smith,,,67890,,1990-02-02,123@gmail.com\n')
    def test_open(self, mock_file):
        self.db.set_filepath('test.csv')
        self.db.open()
        self.assertEqual(len(self.db.addresses), 2)
        self.assertEqual(self.db.addresses[1].firstname, 'John')
        self.assertEqual(self.db.addresses[2].lastname, 'Smith')

    @patch('builtins.open', new_callable=mock_open)
    def test_save(self, mock_file):
        self.db.set_filepath('test.csv')
        address = Address(firstname='John', lastname='Doe', email='123@gmail.com')
        self.db.add_address(address)
        self.db.save()
        handle = mock_file()
        written_data = ''.join([call[0][0] for call in handle.write.call_args_list])
        # Check that the correct CSV header with 'id' was written
        self.assertIn('id,firstname,lastname,street,number,postal_code,place,birthdate,phone,email', written_data.strip())
        # Check that the data was written correctly
        self.assertIn('1,John,Doe,,,,,,,123@gmail.com', written_data.strip())

    def test_add_address(self):
        address = Address(firstname='John', lastname='Doe', email='123@gmail.com')
        self.assertEqual(self.db.add_address(address), 1)
        self.assertTrue(self.db.is_duplicate(address))

    def test_delete(self):
        address = Address(firstname='John', lastname='Doe', email='123@gmail.com')
        self.db.add_address(address)
        self.assertEqual(self.db.delete(1), address)
        self.assertIsNone(self.db.delete(1))

    def test_update(self):
        address = Address(firstname='John', lastname='Doe', email='123@gmail.com')
        self.db.add_address(address)
        self.db.update(1, firstname='Jane')
        self.assertEqual(self.db.addresses[1].firstname, 'Jane')

    def test_search(self):
        address1 = Address(firstname='John', lastname='Doe', email='123@gmail.com')
        address2 = Address(firstname='Jane', lastname='Smith', email='123@gmail.com')
        self.db.add_address(address1)
        self.db.add_address(address2)
        results = self.db.search('firstname', 'Jane')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[2].lastname, 'Smith')


if __name__ == '__main__':
    unittest.main()
