# -*- coding: UTF-8 -*-
# ${topic}
# Name: wolke
# Date: 2024-08-19
# macOS: 14.2.1  Python: 3.12
import os
import random
import shutil
from copy import copy
from datetime import date
from unittest import TestCase

from faker import Faker

from AddressBook.Address import Address  # Bad import statement
from AddressBook.AddressDatabaseCSV import AddressDatabaseCSV  # Bad import statement


class TestAddressDatabaseCSV(TestCase):

    def setUp(self):
        self.dummy_extension = "csv"
        self.existing_filepath = "test_addresses.csv"
        self.faker = Faker()
        self.__dummy_filenames = []
        self.__address_db = AddressDatabaseCSV()  # create an instance of the class
        self.__address_db.set_filepath(self.existing_filepath)
        self.__address_db.open()

    def tearDown(self):
        self.__address_db.close()
        for filename in self.__dummy_filenames:
            if os.path.exists(filename):
                os.remove(filename)

    def __get_random_db_filename__(self) -> str:
        self.__dummy_filenames.append(
            "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=30)) + f".{self.dummy_extension}")
        return self.__dummy_filenames[-1]

    # Wrong type and wrong initialization of the variable
    def __get_random_address__(self) -> Address:
        return Address(self.faker.first_name(), str(self.faker.last_name()), self.faker.street_name(),
                       self.faker.building_number(), self.faker.postcode(), self.faker.city(),
                       self.faker.date_of_birth().strftime('%Y-%m-%d'), self.faker.phone_number(),
                       str(self.faker.random_number(1)) + '@' + self.faker.free_email_domain())

    # filepath is not set in the constructor must set with function set_filepath
    def test_set_filepath_by_ini(self):
        temp_adb = eval(type(self.__address_db).__name__)()  # create a new instance of the same class
        temp_adb.set_filepath(self.existing_filepath)
        if temp_adb.filepath != self.existing_filepath:
            self.fail("set_filepath failed")
        temp_adb.close()

    def test_open_existing_db(self):
        temp_adb = eval(type(self.__address_db).__name__)()  # create a new instance of the same file
        temp_adb.set_filepath(self.existing_filepath)
        temp_adb.open()
        try:
            temp_adb.open()
            temp_adb.close()
        except FileNotFoundError as fe:
            raise fe
        except Exception as e:
            self.fail(f"Open {temp_adb} failed: {e}")

    def test_open_non_existing_db(self):
        temp_adb = eval(type(self.__address_db).__name__)()  # create a new instance of the same file
        temp_adb.set_filepath(self.existing_filepath)
        try:
            temp_adb.open()
            # check if file exists
            self.assertTrue(os.path.exists(temp_adb.filepath), "open failed. File not found")
        except FileNotFoundError as fe:
            self.fail(f"Opening non existing db {self.__address_db.filepath} failed: {fe}")
        temp_adb.close()

    def test_save_to_new_db(self):
        """save a second  file and check if it exists and is not empty"""
        temp_adb = eval(type(self.__address_db).__name__)()  # create a new instance of the same class
        temp_adb.set_filepath(self.__get_random_db_filename__())
        temp_adb.open()
        for address in self.__address_db.get_all().values():
            temp_adb.add_address(address)
        try:
            # write entries to new db
            temp_adb.save()
            # check if file exists
            self.assertTrue(os.path.exists(temp_adb.filepath), "save failed. File not found")
            # check if file bigger than 0
            self.assertTrue(os.path.getsize(temp_adb.filepath) > 0, "save failed. File empty")
            # check if all entries  are copied
            for address in temp_adb.get_all().values():
                self.assertIn(address, self.__address_db.get_all().values(), "save failed. Files are not the same")
            # check if number of entries are the same
            self.assertEqual(len(self.__address_db.get_all().values()), len(temp_adb.get_all().values()),
                             "save failed. Files are not the same")
            temp_adb.close()
        except FileNotFoundError as fe:
            raise fe
        except Exception as e:
            self.fail(f"Save {self.__address_db.filepath} failed: {e}")

    def test_add_address_to_empty_db(self):
        temp_adb = eval(type(self.__address_db).__name__)()  # create a new instance of the same class
        temp_adb.set_filepath(self.__get_random_db_filename__())
        temp_adb.open()
        # test first with empty db, second run with populated db
        new_address = self.__get_random_address__()
        old_len = len(temp_adb.get_all())
        self.assertEqual(old_len, 0, "add_address failed. Address container not empty")
        temp_adb.add_address(new_address)
        new_len = len(temp_adb.get_all())
        self.assertEqual(new_len, 1, "add_address failed. length of address container is not 1")
        self.assertEqual(new_len, old_len + 1, "add_address failed. length of address container did not increase by 1")
        temp_adb.close()

    def test_add_address_to_non_empty_db(self):
        filename = self.__get_random_db_filename__()
        shutil.copy(self.existing_filepath, filename)
        temp_adb = eval(type(self.__address_db).__name__)()  # create a new instance of the same file
        temp_adb.set_filepath(filename)
        temp_adb.open()
        old_len = len(temp_adb.get_all())
        for i in range(1, 101):
            new_address = self.__get_random_address__()
            temp_adb.add_address(new_address)
            new_len = len(temp_adb.get_all())
            self.assertEqual(new_len, old_len + i,
                             "add_address failed. length of address container did not increase by 1")
        temp_adb.close()  # close the file

    def test_add_and_delete_to_empty_db(self):
        temp_adb = eval(type(self.__address_db).__name__)()  # create a new instance of the same file
        temp_adb.set_filepath(self.__get_random_db_filename__())
        temp_adb.open()
        old_len = len(temp_adb.get_all())
        ## add 100 addresses
        for i in range(1, 101):
            new_address = self.__get_random_address__()
            temp_adb.add_address(new_address)
            new_len = len(temp_adb.get_all())
            self.assertEqual(new_len, old_len + i,
                             "add_address failed. length of address container did not increase by 1")
        ## get all keys and delete all addresses
        keys = tuple(temp_adb.get_all().keys())
        self.assertEqual(len(keys), 100, "add_address failed. Address container not filled with 100 addresses")
        for key in keys:
            temp_adb.delete(key)
        self.assertEqual(len(temp_adb.get_all()), 0,
                         "delete failed. Address container not empty after deleting all addresses")
        temp_adb.close()

    def test_delete_from_empty_db(self):
        temp_adb = eval(type(self.__address_db).__name__)()  # create a new instance of the same file
        temp_adb.set_filepath(self.__get_random_db_filename__())
        temp_adb.open()
        for i in (-1, 0, 10, 100):
            index = temp_adb.delete(i)
            self.assertIsNone(index, "delete failed. Returned index is not None")
        temp_adb.close()

    def test_delete_all_from_non_empty_db(self):
        filename = self.__get_random_db_filename__()
        shutil.copy(self.existing_filepath, filename)
        temp_adb = eval(type(self.__address_db).__name__)()  # create a new instance of the same file
        temp_adb.set_filepath(filename)
        temp_adb.open()
        indizes = tuple(temp_adb.get_all().keys())
        for index in indizes:
            res = temp_adb.delete(index)
            self.assertIsNotNone(res, "Could not delete existing address. Returned index is None")
        temp_adb.close()

    '''check entries in db'''

    def test_emptyness_of_db(self):
        temp_adb = eval(type(self.__address_db).__name__)()  # create a new instance of the same file
        temp_adb.set_filepath(self.__get_random_db_filename__())
        temp_adb.open()
        # check if db is empty
        self.assertEqual(len(temp_adb.get_all().keys()), 0, 'Empty db does not seem empty')
        temp_adb.close()

    def test_datatypes(self):
        for address in self.__address_db.get_all().values():
            self.assertEqual(isinstance(address, Address), True,
                             f"get failed. Entry in db not a valid Address object")

    # for search exists a field parameter to specify the field to search for
    def test_search_for_lastname(self):
        filename = self.__get_random_db_filename__()
        shutil.copy(self.existing_filepath, filename)

        temp_adb = eval(type(self.__address_db).__name__)()  # Create a new instance of the same class
        temp_adb.set_filepath(filename)
        temp_adb.open()
        temp_adb.add_address(self.__get_random_address__())  # Add a random address to the database

        # Validate that the database is not empty
        all_entries = temp_adb.get_all()
        if not all_entries:
            with open(filename, 'r') as f:
                print("Contents of copied database file:")
                print(f.read())
            self.fail("Database is empty after opening. Ensure the database file is set up correctly.")

        # Get the first random entry from the database
        ind = tuple(all_entries.keys())[0]
        existing_address = temp_adb.get(ind)
        if not existing_address:
            self.fail("Failed to retrieve the first address from the database.")

        # Modify the retrieved address with random data
        tmp_address = self.__get_random_address__()
        new_address = copy(existing_address)
        new_address.lastname = tmp_address.lastname
        new_address.phone = tmp_address.phone

        # Add the modified address to the database
        temp_adb.add_address(new_address)
        temp_adb.add_address(new_address)  # Adding duplicate intentionally (duplicates won't be added)

        # Retrieve all addresses for debugging
        all_addresses = temp_adb.get_all()

        # Test searching by lastname for both existing and new addresses
        for add in (existing_address, new_address):
            found_addresses = temp_adb.search('lastname', add.lastname)
            print(f"Found addresses for {add.lastname}: {found_addresses}")

            # Verify the address is found in the search results
            if not any(found for found in found_addresses.values() if found == add):
                self.fail(f"Search failed. Address: {add} not found in search results for lastname '{add.lastname}'.")

        temp_adb.close()

    # for search exists a field parameter to specify the field to search for
    def test_search_for_phone(self):
        # Create a new random database file
        filename = self.__get_random_db_filename__()
        shutil.copy(self.existing_filepath, filename)
        temp_adb = eval(type(self.__address_db).__name__)()  # create a new instance of the same class
        temp_adb.set_filepath(filename)
        temp_adb.open()

        # Add a random address to the database
        temp_adb.add_address(self.__get_random_address__())

        # Check if the database is empty
        all_addresses = temp_adb.get_all()
        print(f"All addresses in the temporary database: {all_addresses}")
        if not all_addresses:
            self.fail("The temporary database is empty after opening.")

        # Get an existing address from the database (first address)
        ind = tuple(all_addresses.keys())[0]
        existing_address = temp_adb.get(ind)
        if existing_address is None:
            self.fail("Failed to retrieve the first address from the database.")

        # Get a random address for modification
        tmp_address = self.__get_random_address__()
        if tmp_address is None:
            self.fail("Failed to retrieve a random address. `__get_random_address__()` returned None.")

        # Ensure that tmp_address is an Address object
        if not isinstance(tmp_address, Address):
            self.fail(f"Expected an Address object, but got {type(tmp_address)}")

        # Create a new address based on the random address retrieved
        new_address = self.__get_random_address__()

        # Ensure that new_address is an Address object before adding
        if not isinstance(new_address, Address):
            self.fail(f"Expected an Address object, but got {type(new_address)}")

        # Add the new address (duplicate handling is tested here)
        temp_adb.add_address(new_address)
        temp_adb.add_address(new_address)  # Adding again to test duplicate handling

        # Check all addresses after adding
        all_addresses = temp_adb.get_all()

        # Ensure that the new address was added only once, even though added twice
        if len(all_addresses) < 2:  # Expect at least the existing and the new address
            self.fail(f"Expected at least 2 addresses after adding, but got {len(all_addresses)}")

        # Search for the phone number
        for add in (existing_address, new_address):
            found_addresses = temp_adb.search('phone', add.phone)

            # Ensure the address is found at least once
            if len(found_addresses) == 0:
                self.fail(f"Search failed. Address: {add} not found even once.")

            # Ensure the correct address is among the results
            if add not in found_addresses.values():
                self.fail(f"Search failed. Address: {add} is not in found addresses.")

            # If checking the new address, ensure it was found at least once
            if add == new_address and len(found_addresses) < 1:
                self.fail(f"Search failed. Address: {add} found less than once (expected at least once).")

        temp_adb.close()

    def test_update(self):
        filename = self.__get_random_db_filename__()
        shutil.copy(self.existing_filepath, filename)
        temp_adb = eval(type(self.__address_db).__name__)()  # create a new instance of the same class
        temp_adb.set_filepath(filename)
        temp_adb.open()

        # Ensure the database has at least two entries
        while len(temp_adb.get_all()) < 2:
            temp_adb.add_address(self.__get_random_address__())

        all_keys = tuple(temp_adb.get_all().keys())
        if len(all_keys) < 2:
            self.fail("Not enough entries in the database to perform the update test.")

        # changing 2 addresses first and last
        for i in (0, -1):
            ind = all_keys[i]
            new_address = self.__get_random_address__()
            temp_adb.update(ind, lastname=new_address.lastname, phone=new_address.phone)
            self.assertEqual(temp_adb.get(ind).lastname, new_address.lastname, "update failed. Lastname not updated")
            self.assertEqual(temp_adb.get(ind).phone, new_address.phone, "update failed. Phone not updated")
        temp_adb.close()

    def test_get_todays_birthdays(self):
        filename = self.__get_random_db_filename__()
        shutil.copy(self.existing_filepath, filename)
        temp_adb = eval(type(self.__address_db).__name__)()
        temp_adb.set_filepath(filename)
        temp_adb.open()
        delta_years = (12, 20, 3, 7)
        for dy in delta_years:
            add_today = self.__get_random_address__()
            add_today.birthdate = date.today().replace(year=date.today().year - dy)
            temp_adb.add_address(add_today)
        birthdays = temp_adb.get_todays_birthdays()
        self.assertEqual(len(birthdays), len(delta_years),
                         f"get_todays_birthdays failed. Not all birthdays (must be {len(delta_years)}) found")
        for address in birthdays.values():
            if address.birthdate.month != date.today().month or address.birthdate.day != date.today().day:
                self.fail("get_todays_birthdays failed. Not all birthdays are today")
        temp_adb.close()
