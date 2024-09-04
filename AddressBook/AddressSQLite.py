import AddressContainerInterface
import AddressBook
import sqlite3
import os
import tkinter as tk
from tkinter import filedialog

class AddressSQLite(AddressContainerInterface.AddressContainerInterface):
    def __init__(self, mode = 1):
        self.filepath = filedialog.askopenfilename()
        self.conn = sqlite3.connect(self.filepath)
        self.cursor = self.conn.cursor()

    def set_filepath(self, mode: bool = 1):
        root = tk.Tk()
        root.withdraw()

        if mode:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".db",
                filetypes=[("SQLite database files", "*.db"), ("All files", "*.*")]
            )
            try:
                print(f"Created file at {filepath}")
            except:
                print("Failed to create file")

        else:
            filepath = filedialog.askopenfilename(
                title="Select SQLite Database File",
                filetypes=[("SQLite Database Files", "*.db *.sqlite *.sqlite3"), ("All Files", "*.*")]
            )
            try:
                print(f"Opened file {filepath}")
            except:
                print("Failed to open file")

        return filepath

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

    def setup_tables(self):
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS AddressBook (
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


a = AddressSQLite()
a.setup_tables()