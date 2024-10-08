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
        self.filepath = filepath

    def open(self):
        with open(self.filepath, "a"):
            try:
                self.conn = sqlite3.connect(self.filepath)
                self.cursor = self.conn.cursor()
                self.setup_tables()
            except sqlite3.Error as e:
                print(f"Error Code {e.sqlite_errorcode}: {e.sqlite_errorname}")
            except Exception as e:
                print(e)

    def close(self):
        try:
            if self.conn:
                self.cursor.close()
                self.conn.close()
        except sqlite3.Error as e:
            print(f"Error Code {e.sqlite_errorcode}: {e.sqlite_errorname}")

    def save(self):
        try:
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error Code {e.sqlite_errorcode}: {e.sqlite_errorname}")

    def search(self, search_string: str, field: str = "") -> dict[int, AddressBook]:
        columns = ["first_name", "last_name", "street", "number",
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

    def add_address(self, address: AddressBook) -> int:
        try:
            self.cursor.execute(f'''
                        INSERT INTO {self.tablename} (first_name, last_name, street, 
                        number, postal_code, place, birthdate, phone, email)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', address)
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error:
            return False

    def get_all(self) -> dict[int, AddressBook]:
        self.cursor.execute(f"SELECT * FROM {self.tablename}")
        return {elements[0]: elements[1:] for elements in self.cursor.fetchall()}

    def get(self, address_id: int) -> AddressBook:
        self.cursor.execute(f"SELECT * FROM {self.tablename} WHERE id = {address_id}")
        return {elements[0]: elements[1:] for elements in self.cursor.fetchall()}

    def get_todays_birthdays(self) -> dict[int, AddressBook]:
        self.cursor.execute(f"SELECT * FROM {self.tablename} "
                            f"WHERE strftime('%m-%d', birthdate) = strftime('%m-%d', 'now');")
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


if __name__ == '__main__':
    a = AddressSQLite()
    a.set_filepath(r"..\AddressBook\SQLite\addressbook.db")
    print(a.filepath)
    a.open()
    a.save()
    print(a.get_all())
    print(a.search("Henri"))
    a.delete(2)
    print(a.get(1))
    a.update(2, birthdate="2005-06-26")
    print(a.get(2))
    b = AddressBook(firstname="Domink", lastname="Hase")
    a.add_address(b)
    print(a.get(3))
    a.update(3, birthdate="2006-08-10")
    print(a.get_todays_birthdays())
