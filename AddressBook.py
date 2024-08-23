from datetime import datetime, date
from pydantic.dataclasses import dataclass
from pydantic import field_validator, PositiveInt
from typing import Optional
from dataclasses import field
from email_validator import validate_email, EmailNotValidError, EmailSyntaxError


@dataclass(order=True)
class AddressBook:
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
    def validate_birthdate(cls, value) -> date:
        return datetime.strptime(value, "%Y-%m-%d").date()

    @field_validator('email')
    def get_validate_email(cls, value):
        try:
            validate_email(value, check_deliverability=True)
            return value
        except EmailSyntaxError as e:
            print('Email syntax error', e)
        except EmailNotValidError as e:
            raise e

    def __str__(self):
        return (f"Name: {self.firstname} {self.lastname} {self.birthdate}\nAddress: {self.street} {self.number}, {self.postal_code} "
                f"{self.place}\nContact: {self.phone} {self.email}\n")


if __name__ == '__main__':
    a1 = AddressBook('Henri', 'Henrison', 'ABC-Street', '10', 11111, 'Berlin', '2001-12-01', '12345678',
                     '123@gmail.com')
    a2 = AddressBook('Henri', 'Henrison', 'ABC-Street', '12a', 11111, 'Berlin')

    a3 = AddressBook('Henri', 'Henrison', 'ABC-Street', '10', 11111, 'Berlin', '2001-12-01', '12345678',
                     'a@mail.com')

    print(a1)
    print(a2)
    print(a1 > a2)

    l = [a1, a2, a3]
    sorted_list = sorted(l)
    for element in sorted_list:
        print(element)
