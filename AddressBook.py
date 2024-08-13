from dataclasses import dataclass
from datetime import datetime, date

@dataclass(order=True)
class Address:
    firstname: str
    lastname: str
    street: str = ''
    number: str = ''
    postal_code: int = 0 
    place: str = ''
    birthday: date = '0001-01-01'
    phone: str = ""
    email: str = ""

    def __post_init__(self):
        self.birthday: date = datetime.strptime(self.birthday, "%Y-%m-%d").date()

    def __str__(self):
        return f"Name: {self.firstname} {self.lastname}\nAddress: {self.street} {self.number}, {self.postal_code} {self.place}\nContact: {self.phone} {self.email}\n"






if __name__ == '__main__':
    a1 = Address('Henri', 'Henrison', 'ABC-Street', '10', 11111, 'Berlin', '2001-12-01', '12345678', 'a@mail.com')
    a2 = Address('Henri', 'Henrison', 'ABC-Street', '12a', 11111, 'Berlin')
    a3 = Address('Henri', 'Henrison', 'ABC-Street', '10', 11111, 'Berlin', '2001-12-01', '12345678', 'a@mail.com')
    

    
    print(a1)
    print(a2)
    print(a1 > a2)
    l = [a1, a2, a3]
    sorted_list = sorted(l)
    for element in sorted_list:
        print(element)