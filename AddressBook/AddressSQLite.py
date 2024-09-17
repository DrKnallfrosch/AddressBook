from AddressContainerInterface import AddressContainerInterface
import AddressBook
import sqlite3


class AddressSQLite(AddressContainerInterface):
    def __init__(self, filepath:str = None, tablename="AddressBook"):

        self.filepath = filepath
        self.conn = None
        self.cursor = None
        self.tablename = tablename

    def set_filepath(self, filepath: str):
        self.filepath = filepath

    def open(self):
        with open(self.filepath, "a"):
            try:
                self.conn = sqlite3.connect(self.filepath)
                self.cursor = self.conn.cursor()
            except sqlite3.Error as e:
                print(f"Error Code {e.sqlite_errorcode}: {e.sqlite_errorname}")

    def close(self):
        self.cursor.close()
        self.conn.close()

    def save(self):
        pass # might need implementation

    def search(self, search_string: str) -> dict:
        columns = ["id", "first_name", "last_name", "street", "number",
                   "postal_code", "place", "birthdate", "phone", "email"]
        columns = f" LIKE '%{search_string}%' OR ".join(columns)
        self.cursor.execute(f"SELECT * FROM {self.tablename} WHERE {columns} LIKE '%{search_string}%';")
        return {elements[0]: elements[1:] for elements in self.cursor.fetchall()}

    def delete(self, address_id: int) -> int:
        try:
            self.cursor.execute(f"DELETE FROM {self.tablename} WHERE id = {address_id}")
            self.conn.commit()
            return address_id
        except sqlite3.Error:
            return False

    def update(self, address_id: int, **kwargs) -> int:
        fields = ', '.join([f"{key} = ?" for key in kwargs])
        values = list(kwargs.values()) + [address_id]
        try:
            self.cursor.execute(f"UPDATE {self.tablename} SET {fields} WHERE id = ?", values)
            self.conn.commit()
            return address_id
        except sqlite3.Error:
            raise KeyError

    def add_address(self, data: tuple) -> int:
        try:
            self.cursor.execute(f'''
                        INSERT INTO {self.tablename} (first_name, last_name, street, number, postal_code, place, birthdate, phone, email)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error:
            return False

    def get_all(self) -> dict:
        self.cursor.execute(f"SELECT * FROM {self.tablename}")
        return {elements[0]: elements[1:] for elements in self.cursor.fetchall()}

    def get(self, address_id: int) -> AddressBook:
        self.cursor.execute(f"SELECT * FROM {self.tablename} WHERE id = {address_id}")
        return {elements[0]: elements[1:] for elements in self.cursor.fetchall()}

    def get_todays_birthdays(self) -> dict:
        self.cursor.execute(f"SELECT * FROM {self.tablename} WHERE strftime('%m-%d', birthdate) = strftime('%m-%d', 'now');")
        return {elements[0]: elements[1:] for elements in self.cursor.fetchall()}

    def setup_tables(self):
        self.cursor.execute(f'''
            CREATE table IF NOT EXISTS {self.tablename} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                street TEXT,
                number TEXT,
                postal_code TEXT,
                place TEXT,
                birthdate TEXT,
                phone TEXT,
                email TEXT);
        ''')
        self.conn.commit()

a = AddressSQLite(filepath=r"..\AddressBook\SQLite\addressbook.mp4", tablename="AddressBook")
a.setup_tables()
print(a.get_todays_birthdays())