from AddressBook.Address import Address
from AddressBook.AddressDatabaseCSV import AddressDatabaseCSV
from AddressBook.AddressDatabaseSQL import AddressDatabaseSQL


def display_menu():
    print("\n--- Address Book Menu ---")
    print("0. Set Filepath")
    print("1. Add Address")
    print("2. Search Address")
    print("3. Update Address")
    print("4. Delete Address")
    print("5. Show All Addresses")
    print("6. Show Today's Birthdays")
    print("7. Exit")


def set_filepath(addressdb):
    filepath = input("Enter the new filepath: ")
    addressdb.set_filepath(filepath)
    print(f"Filepath set to: {filepath}")
    addressdb.open()


def add_address(address_db):
    firstname = input("Enter First Name: ")
    lastname = input("Enter Last Name: ")
    street = input("Enter Street: ")
    number = input("Enter House Number: ")
    postal_code = input("Enter Postal Code: ")
    place = input("Enter Place: ")
    birthdate = input("Enter Birthdate (YYYY-MM-DD): ")
    phone = input("Enter Phone Number: ")
    email = input("Enter Email: ")

    if postal_code == "":
        postal_code = None

    new_address = Address(
        firstname=firstname,
        lastname=lastname,
        street=street,
        number=number,
        postal_code=postal_code,
        place=place,
        birthdate=birthdate,
        phone=phone,
        email=email
    )

    address_id = address_db.add_address(new_address)
    if address_id == -1:
        print("This address already exists.")
    else:
        print(f"Address added with ID: {address_id}")


def search_address(address_db):
    field = input("Enter the field to search by (firstname/lastname/email): ")
    search_string = input("Enter the search string: ")
    results = address_db.search(field, search_string)

    if results:
        print("Search Results:")
        for id_, address in results.items():
            print(address)
    else:
        print("No matching addresses found.")


def update_address(address_db):
    address_id = int(input("Enter the ID of the address to update: "))
    updates = {}
    if address_id in address_db.get_all():
        field = input(
            "Enter the field to update (firstname/lastname/street/number/postal_code/place/birthdate/phone/email): ")
        value = input(f"Enter the new value for {field}: ")
        updates[field] = value

        address_db.update(address_id, **updates)
        print(f"Address with ID {address_id} updated.")
    else:
        print(f"No address found with ID {address_id}.")


def delete_address(address_db):
    address_id = int(input("Enter the ID of the address to delete: "))
    deleted_id = address_db.delete(address_id)
    if deleted_id is not None:
        print(f"Address with ID {deleted_id} deleted.")
    else:
        print(f"No address found with ID {address_id}.")


def show_all_addresses(address_db):
    print("All Addresses:")
    for id_, address in address_db.get_all().items():
        print(address)


def show_a_address(address_db):
    id_ = int(input("Enter the specific id"))
    print(address_db.get(id_))


def show_todays_birthdays(address_db):
    birthdays_today = address_db.get_todays_birthdays()
    if birthdays_today:
        print("Today's Birthdays:")
        for id_, address in birthdays_today.items():
            print(f"ID: {id_}, Name: {address.firstname} {address.lastname}, Birthdate: {address.birthdate}")
    else:
        print("No birthdays today.")


def choose_database():
    while True:
        db_choice = input("Choose database model (CSV/SQL): ").strip().lower()
        if db_choice == 'csv':
            return AddressDatabaseCSV()
        elif db_choice == 'sql':
            return AddressDatabaseSQL()
        else:
            print("Invalid choice. Please choose 'CSV' or 'SQL'.")


if __name__ == '__main__':
    address_db = choose_database()  # Ask user to choose the database model

    while True:
        display_menu()
        choice = input("Choose an option: ")

        if choice == '1':
            set_filepath(address_db)
        elif choice == '2':
            add_address(address_db)
            address_db.save()
        elif choice == '3':
            search_address(address_db)
        elif choice == '4':
            update_address(address_db)
            address_db.save()
        elif choice == '5':
            delete_address(address_db)
            address_db.save()
        elif choice == '6':
            show_all_addresses(address_db)
        elif choice == '7':
            show_a_address(address_db)
        elif choice == '8':
            show_todays_birthdays(address_db)
        elif choice == '9':
            address_db.close()
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
