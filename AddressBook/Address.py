from dataclasses import field
from datetime import datetime, date
from typing import Optional
from email_validator import validate_email, EmailNotValidError
from pydantic import field_validator, PositiveInt
from pydantic.dataclasses import dataclass


@dataclass(order=True)
class Address:
    """
    Represents an entry in the address book.

    NOTE: Only numerical postal codes are permitted.

    :ivar firstname: The first name of the person.
    :type firstname: str
    :ivar lastname: The last name of the person.
    :type lastname: str
    :ivar street: The street where the person lives.
    :type street: Optional[str]
    :ivar number: The house number of the person.
    :type number: Optional(str)
    :ivar postal_code: The postal code of the person's address.
    :type postal_code: Optional(PositiveInt)
    :ivar place: The city where the person lives.
    :type place: Optional(str)
    :ivar birthdate: The birthdate of the person.
    :type birthdate: Optional(str)
    :ivar phone: The phone number of the person.
    :type phone: Optional(str)
    :ivar email: The email address of the person.
    :type email: Optional(str)
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

        :param str value: The birthdate string in 'YYYY-MM-DD' format.
        :return: The birthdate as a `datetime.date` object if valid, or None if the value is empty.
        :rtype: Optional[date]
        :raises ValueError: If the birthdate string is not in the correct format.
        """
        if value is None or value == '':
            return None
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(f"Invalid birthdate format: {value}")

    @field_validator('email')
    def validate_email(cls, value: Optional[str]) -> Optional[str]:
        """
        Validates the email address using the `email_validator` library.
        checks if the email format is valid and if the email is deliverable.

        :param Optional[str] value: The email address to validate.
        :return: The validated email address, or None if the value is empty.
        :rtype: Optional[str]
        :raises ValueError: If the email format is invalid.
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

        :return: A formatted string containing the full details of the address book entry.
        :rtype: str
        """
        return (
            f"Name: {self.firstname} {self.lastname} {self.birthdate}\n"
            f"Address: {self.street} {self.number}, {self.postal_code} {self.place}\n"
            f"Contact: {self.phone} {self.email}\n")
