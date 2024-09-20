from dataclasses import field
from datetime import datetime, date
from typing import Optional
from email_validator import validate_email, EmailNotValidError
from pydantic import field_validator, PositiveInt
from pydantic.dataclasses import dataclass


@dataclass(order=True)
class AddressBook:
    """
    Represents an entry in the address book.

    Attributes:
        firstname (str): The first name of the person.
        lastname (str): The last name of the person.
        street (Optional[str]): The street where the person lives.
        number (Optional[str]): The house number of the person.
        postal_code (Optional[PositiveInt]): The postal code of the person's address.
        place (Optional[str]): The city or town where the person lives.
        birthdate (Optional[str]): The birthdate of the person in 'YYYY-MM-DD' format.
        phone (Optional[str]): The person's phone number.
        email (Optional[str]): The person's email address.
    """

    firstname: str
    lastname: str
    street: Optional[str] = field(default=None)
    number: Optional[str] = field(default=None)
    postal_code: Optional[PositiveInt] = field(default=None)
    place: Optional[str] = field(default=None)
    birthdate: Optional[str] = field(default=None)
    phone: Optional[str] = field(default=None)
    email: Optional[str] = field(default=None)

    @field_validator('birthdate')
    def validate_birthdate(cls, value) -> Optional[date]:
        """
        Validates and converts the birthdate string into a `datetime.date` object.

        Args:
            value (str): The birthdate string in 'YYYY-MM-DD' format.

        Returns:
            Optional[date]: The birthdate as a `datetime.date` object if valid, or None if the value is empty.

        Raises:
            ValueError: If the birthdate string is not in the correct format.
        """
        if value is None or value == '':
            return None
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(f"Invalid birthdate format: {value}")

    @field_validator('email')
    def get_validate_email(cls, value: Optional[str]) -> Optional[str]:
        """
        Validates the email address using the `email_validator` library.

        Args:
            value (str): The email address to validate.

        Returns:
            Optional[str]: The validated email address, or None if the value is empty.

        Raises:
            ValueError: If the email format is invalid.
        """
        if value is None or value == '':
            return None  # Return None if email is empty or missing
        try:
            validate_email(value, check_deliverability=True)
            return value
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email format: {value}")

    def __str__(self):
        """
        Returns a string representation of the address book entry.

        Returns:
            str: A formatted string containing the full details of the address book entry.
        """
        return (
            f"Name: {self.firstname} {self.lastname} {self.birthdate}\n"
            f"Address: {self.street} {self.number}, {self.postal_code} {self.place}\n"
            f"Contact: {self.phone} {self.email}\n"
        )


if __name__ == '__main__':
    a1 = AddressBook('Henri', 'Henrison', 'ABC-Street', '10', 11111, 'Berlin', '2001-12-01', '12345678',
                     '123@gmail.com')
    a2 = AddressBook('Henri', 'Henrison', 'ABC-Street', '12a', 11111, 'Berlin')

    a3 = AddressBook('Henri', 'Henrison', 'ABC-Street', '10', 11111, 'Berlin', '2001-12-01', '12345678',
                     'a@mail.com')
    a4 = AddressBook("Niki", "Fresse")

    print(a1)
    print(a2)
    print(a1 > a2)

    l = [a1, a2, a3]
    sorted_list = sorted(l)
    for element in sorted_list:
        print(element)

    print(a4)
