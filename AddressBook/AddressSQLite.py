import sqlite3
import tkinter as tk
from tkinter import filedialog

import AddressBook
from AddressContainerInterface import AddressContainerInterface


class AddressSQLite(AddressContainerInterface):
    def __init__(self, mode=True, table="AddressBook"):
        self.filepath = self.set_filepath(mode)
        self.conn = sqlite3.connect(self.filepath)
        self.cursor = self.conn.cursor()
        self.table = table

    def set_filepath(self, mode: bool = 1):
        root = tk.Tk()
        root.withdraw()

        if mode:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".db",
                filetypes=[("SQLite database files", "*.db"), ("All files", "*.*")]
            )
            print(f"Created file at {filepath}")

        else:
            filepath = filedialog.askopenfilename(
                title="Select SQLite Database File",
                filetypes=[("SQLite Database Files", "*.db *.sqlite *.sqlite3"), ("All Files", "*.*")]
            )
            print(f"Opened file {filepath}")
        return filepath

    def read(self):
        pass

    def save(self):
        pass

    def search(self, search_string: str, columns: list = ["all"], exact: bool = 0) -> dict:
        if columns == ["all"]:
            columns = ["id", "first_name", "last_name", "street", "number",
                       "postal_code", "place", "birthdate", "phone", "email"]
        columns = f" LIKE '%{search_string}%' OR ".join(columns)
        self.cursor.execute(f"SELECT * FROM {self.table} WHERE {columns} LIKE '%{search_string}%';")
        data = {}
        print(self.cursor.fetchall()[0])
        for i in self.cursor.fetchall():
            data.update({i[0]: i[1:]})
        return data

    def add_address(self, data) -> int:

        self.cursor.execute(f'''
        INSERT INTO {self.table} (first_name, last_name, street, number, postal_code, place, birthdate, phone, email)
        VALUES ()''')

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

    def setup_tables(self):
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                street TEXT,
                number TEXT,
                postal_code TEXT,
                place TEXT,
                birthdate TEXT,
                phone TEXT,
                email TEXT
            );
        ''')
        self.conn.commit()


a = AddressSQLite(mode=0, table="AddressBook")
a.setup_tables()
print(a.search(input("Search string: ")))
