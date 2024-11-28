# Address Book Application

## Overview

This Address Book application allows users to manage their contacts efficiently. Users can add, update, delete, and search for addresses. The application supports both CSV and SQL database models for storing the address data.

## Features

- Add new addresses
- Update existing addresses
- Delete addresses
- Search for addresses by various fields
- Display all addresses
- Show today's birthdays
- Choose between CSV and SQL database models

## Requirements

- Python 3.8+
- `email_validator` library
- `pydantic` library

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/DrKnallfrosch/address-book.git
    cd address-book
    ```

2. Install the required Python packages:
    ```sh
    pip install -r req.txt
    ```

## Usage

1. Run the application:
    ```sh
    python main.py
    ```

2. Follow the on-screen instructions to choose the database model and perform various operations.

## Running Tests

To run the tests, use the following command:
```sh
python -m unittest discover tests
```

## Project Structure

- `main.py`: The main entry point of the application.
- `AddressBook/Address.py`: Contains the `Address` dataclass.
- `AddressBook/AddressDatabaseCSV.py`: Handles CSV database operations.
- `AddressBook/AddressDatabaseSQL.py`: Handles SQL database operations.
- `tests/`: Contains unit tests for the application.

## Documentation

After Installing the repository, you can find the documentation in the `docs/build/html/index.html` file.
you can open the file in your browser to view the documentation and have a better understanding of the project.
