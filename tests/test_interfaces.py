from dataclasses import dataclass
from abc import ABC, abstractmethod
import csv


@dataclass
class Add:
    a: tuple[int, int]

    def add(self):
        return self.a[0] + self.a[1]


class AddInterface(ABC):
    @abstractmethod
    def insert(self) -> tuple[int, int]:
        pass


class AddInterfaceCSV(AddInterface):
    def insert(self) -> tuple[int, int]:
        with open('data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            data = next(reader)  # Read the first row
            a, b = int(data[0]), int(data[1])
            return a, b


# Use the data from the CSV file to create an Add object
csv_adder = AddInterfaceCSV()
b = Add(csv_adder.insert())

# Print the result of the addition
print(b.add())
