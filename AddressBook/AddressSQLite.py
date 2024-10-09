from AddressContainerInterface import AddressContainerInterface
from AddressBook import AddressBook
import sqlite3


class AddressSQLite(AddressContainerInterface):
    def __init__(self, filepath: str = None, tablename="AddressBook"):
        self.filepath = filepath
        self.conn = None
        self.cursor = None
        self.tablename = tablename

    def set_filepath(self, filepath: str):
        """
        Set the file path for the SQL-Database that contains the address data.

        Args:
            filepath (str): The path to the SQL-Database file.
        """
        self.filepath = filepath

    def open(self):
        """
        Establish the connection to the SQL-Database file specified by the filepath attribute and
        creates a cursor object. Calls the setup_table method to create a table (if not already existing)
        with the name specified by the tablename attribute. Outputs the error in case any occur.
        """
        with open(self.filepath, "a"):
            try:
                self.conn = sqlite3.connect(self.filepath)
                self.cursor = self.conn.cursor()
                self.setup_table()
            except sqlite3.Error as e:
                print(f"Error Code {e.sqlite_errorcode}: {e.sqlite_errorname}")
            except Exception as e:
                print(e)

    def close(self):
        """
        Closes the cursor object and the connection to the SQL-Database. Outputs the error in case any occur.
        """
        try:
            if self.conn:
                self.cursor.close()
                self.conn.close()
        except sqlite3.Error as e:
            print(f"Error Code {e.sqlite_errorcode}: {e.sqlite_errorname}")

    def save(self):
        """
        Commits all changes done to the SQL-Database. Outputs the error in case any occur.
        """
        try:
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error Code {e.sqlite_errorcode}: {e.sqlite_errorname}")

    def search(self, search_string: str, field: str = "") -> dict[int, AddressBook]:
        """
        Search for a given string across all fields of the database and returns matching entries.
        Additionally, takes the field string to restrict the search to a specific field.
        The Search is done case-insensitive and non-exact (utilizes the LIKE statement with wildcards).

        Args:
            search_string (str): The string to search for across all fields or restricted to one field.
            field (str, optional): The field to search within (e.g., "firstname", "lastname", "email").
                                   Defaults to an empty string (""), resulting in a search across all fields.

        Returns:
            dict[int, AddressBook]: A dictionary containing matching address entries with IDs as keys.
        """
        columns = ["firstname", "lastname", "street", "number",
                   "postal_code", "place", "birthdate", "phone", "email"]

        if field and field not in columns:
            raise ValueError(f"Invalid field: '{field}'. Must be one of {columns}.")
        elif field:
            query = f"SELECT * FROM {self.tablename} WHERE {field} LIKE ?;"
            self.cursor.execute(query, (f"%{search_string}%",))
        else:
            query = f"SELECT * FROM {self.tablename} WHERE " + " OR ".join(
                [f"{col} LIKE ?" for col in columns]
            ) + ";"
            search_params = [f"%{search_string}%"] * len(columns)
            self.cursor.execute(query, search_params)
        return {elements[0]: AddressBook(*elements[1:]) for elements in self.cursor.fetchall()}

    def delete(self, id_: int) -> int | None:
        """
        Deletes an address by its ID.

        Args:
            id_ (int): The ID of the address to delete.

        Returns:
            int | None: The ID of the deleted address if found and removed, otherwise None.
        """
        try:
            self.cursor.execute(f"DELETE FROM {self.tablename} WHERE id = {id_}")
            self.conn.commit()
            return id_
        except FileNotFoundError as e:
            print(e)
            return None

    def update(self, id_: int, **kwargs) -> int:
        """
        Update fields of an address by its ID and keyword arguments. Raises KeyError if the ID is not found.

        Args:
            id_ (int): The ID of the address to update.
            **kwargs: Field names and their updated values (e.g., firstname="John").

        Returns:
            int: The ID of the updated address.

        Raises:
            KeyError: If the address with the given ID is not found.
        """
        fields = ', '.join([f"{key} = ?" for key in kwargs])
        values = list(kwargs.values()) + [id_]
        try:
            self.cursor.execute(f"UPDATE {self.tablename} SET {fields} WHERE id = {values}")
            self.conn.commit()
            return id_
        except sqlite3.Error:
            raise KeyError

    def add_address(self, address: AddressBook) -> int:
        """
        Add a new address to the address book, ensuring no duplicates are added.

        Args:
            address (AddressBook): The address to add.

        Returns:
            int: The ID of the newly added address, 0 if an error occurs or -1 if it already exists.
        """
        if self.is_duplicate(address):
            print("This address book entry already exists.")
            return -1

        try:
            self.cursor.execute(f'''
                        INSERT INTO {self.tablename} (firstname, lastname, street, 
                        number, postal_code, place, birthdate, phone, email)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                address.firstname,
                address.lastname,
                address.street,
                address.number,
                address.postal_code,
                address.place,
                address.birthdate,
                address.phone,
                address.email
            )
        )
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error:
            print(f"Error adding address: {address}")
            return 0


    def get_all(self) -> dict[int, AddressBook]:
        """
        Return all address entries as a dictionary.

        Returns:
            dict[int, AddressBook]: A dictionary where keys are IDs and values are AddressBook objects.
        """
        self.cursor.execute(f"SELECT * FROM {self.tablename}")
        return {elements[0]: AddressBook(*elements[1:]) for elements in self.cursor.fetchall()}

    def get(self, id_: int) -> AddressBook | None:
        """
        Retrieve an address by its ID.

        Args:
            id_ (int): The ID of the address to retrieve.

        Returns:
            AddressBook | None: The address if found, otherwise None.
        """
        self.cursor.execute(f"SELECT * FROM {self.tablename} WHERE id = {id_}")
        result = self.cursor.fetchone()
        print(result)
        if result:
            return {result[0]: AddressBook(*result[1:])}
        return None



    def get_todays_birthdays(self) -> dict[int, AddressBook]:
        """
        Get all addresses of persons who have their birthday today.

        Returns:
            dict[int, AddressBook]: A dictionary where keys are IDs and values are AddressBook
                                    objects with matching birthdays.
        """
        self.cursor.execute(f"SELECT * FROM {self.tablename} "
                            f"WHERE strftime('%m-%d', birthdate) = strftime('%m-%d', 'now');")
        return {elements[0]: AddressBook(*elements[1:]) for elements in self.cursor.fetchall()}

    def setup_table(self):
        """
        Creates a table in the currently specified filepath with all fields given in the AddressBook dataclass and an
        automatically increasing id as the primary key. Doesn't create in case there already is one with the name in the
        tablename attribute.
        """
        self.cursor.execute(f'''
            CREATE table IF NOT EXISTS {self.tablename} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                street TEXT,
                number INTEGER,
                postal_code TEXT,
                place TEXT,
                birthdate TEXT,
                phone TEXT,
                email TEXT);
        ''')
        self.conn.commit()

    def is_duplicate(self, address: AddressBook) -> bool:
        """
        Check if an address is a duplicate based on first name, last name, and email.

        Args:
            address (AddressBook): The address to check for duplicates.

        Returns:
            bool: True if a duplicate is found, otherwise False.
        """
        self.cursor.execute(f"SELECT id, email FROM {self.tablename} WHERE firstname = ? and lastname = ?;",
                            (address.firstname, address.lastname))
        if self.cursor.fetchall():
            return True
        return False