import unittest
import os
from AddressBook.Address import Address
from AddressBook.AddressDatabaseCSV import AddressDatabaseCSV


class TestAddressDatabaseCSV(unittest.TestCase):

    def setUp(self):
        # Set up file path for testing
        self.test_file = 'test_addressbook.csv'
        self.db = AddressDatabaseCSV()
        self.db.set_filepath(self.test_file)

    def tearDown(self):
        # Clean up by removing the test file after each test
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_open(self):
        # Create a CSV file with test data
        with open(self.test_file, 'w') as f:
            f.write('id,firstname,lastname,street,number,postal_code,place,birthdate,phone,email\n')
            f.write('1,John,Doe,muster,12,12345,bremen,1990-01-01,123@gmail.com\n')
            f.write('2,Jane,Smith,muster,12a,67890,bremen,1990-02-02,123@gmail.com\n')

        # Open the file using the database class
        self.db.open()

        # Assert that the addresses were correctly read
        self.assertEqual(len(self.db.addresses), 2)
        self.assertEqual(self.db.addresses[1].firstname, 'John')
        self.assertEqual(self.db.addresses[2].lastname, 'Smith')

    def test_save(self):
        # Add a new address and save it to the CSV file
        address = Address(firstname='John', lastname='Doe', street='Muster', number='12a', postal_code=1,
                          place='bremen', birthdate='2000-01-01', phone='0123456789', email='123@gmail.com')
        self.db.add_address(address)
        self.db.save()

        # Read the file and check if the data was saved correctly
        with open(self.test_file, 'r') as f:
            written_data = f.read()

        self.assertIn('id,firstname,lastname,street,number,postal_code,place,birthdate,phone,email',
                      written_data.strip())
        self.assertIn('1,John,Doe,muster,12a,1,bremen,2000-01-01,0123456789,123@gmail.com', written_data.strip())

    def test_add_address(self):
        address = Address(firstname='John', lastname='Doe', street='Muster', number='12a', postal_code=1,
                          place='bremen', birthdate='2000-01-01', phone='0123456789', email='123@gmail.com')
        self.assertEqual(self.db.add_address(address), 1)
        self.assertTrue(self.db.is_duplicate(address))

    def test_delete(self):
        address = Address(firstname='John', lastname='Doe', street='Muster', number='12a', postal_code=1,
                          place='bremen', birthdate='2000-01-01', phone='0123456789', email='123@gmail.com')
        self.db.add_address(address)
        self.assertEqual(self.db.delete(1), address)
        self.assertIsNone(self.db.delete(1))

    def test_update(self):
        address = Address(firstname='John', lastname='Doe', street='Muster', number='12a', postal_code=1,
                          place='bremen', birthdate='2000-01-01', phone='0123456789', email='123@gmail.com')
        self.db.add_address(address)
        self.db.update(1, firstname='Jane')
        self.assertEqual(self.db.addresses[1].firstname, 'Jane')

    def test_search(self):
        address1 = Address(firstname='John', lastname='Doe', street='Muster', number='12a', postal_code=1,
                           place='bremen', birthdate='2000-01-01', phone='0123456789', email='123@gmail.com')
        address2 = Address(firstname='Jane', lastname='Smith', street='Muster', number='12a', postal_code=1,
                           place='bremen', birthdate='2000-02-02', phone='9876543210', email='123@gmail.com')
        self.db.add_address(address1)
        self.db.add_address(address2)
        self.db.save()

        results = self.db.search('firstname', 'Jane')

        self.assertEqual(results[2].lastname, 'Smith')  # Access the result by its correct key (2)


if __name__ == '__main__':
    unittest.main()
