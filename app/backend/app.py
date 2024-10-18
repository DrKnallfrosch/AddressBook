from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import csv

app = Flask(__name__, static_folder="../frontend")
CORS(app)  # Allow cross-origin requests

# Path to CSV file
CSV_FILE_PATH = "addresses.csv"


# Helper functions to read and write to CSV
def load_csv():
    """Load all addresses from the CSV file."""
    addresses = []
    if not os.path.exists(CSV_FILE_PATH):
        return addresses  # Return empty list if file doesn't exist
    with open(CSV_FILE_PATH, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['id'] = int(row['id'])  # Ensure ID is an integer
            addresses.append(row)
    return addresses


def save_csv(addresses):
    """Save all addresses to the CSV file."""
    with open(CSV_FILE_PATH, mode='w', newline='') as file:
        fieldnames = ['id', 'firstname', 'lastname', 'street', 'number', 'postal_code', 'place', 'birthday', 'phone', 'email']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(addresses)


def get_next_id(addresses):
    """Get the next available ID."""
    if not addresses:
        return 1
    return max(address['id'] for address in addresses) + 1


# Serve the Vue.js front-end
@app.route('/')
def serve_vue_app():
    return send_from_directory(app.static_folder, 'index.html')


# API Endpoints
@app.route('/api/addresses', methods=['GET'])
def get_all_addresses():
    addresses = load_csv()
    return jsonify(addresses)


@app.route('/api/addresses/<int:id>', methods=['GET'])
def get_address(id):
    addresses = load_csv()
    address = next((a for a in addresses if a['id'] == id), None)
    if address:
        return jsonify(address)
    return jsonify({"error": "Address not found"}), 404


@app.route('/api/addresses', methods=['POST'])
def add_address():
    data = request.json
    addresses = load_csv()

    # Create a new address with the next available ID
    new_address = {
        'id': get_next_id(addresses),
        'firstname': data.get('firstname'),
        'lastname': data.get('lastname'),
        'street': data.get('street'),
        'number': data.get('number'),
        'postal_code': data.get('postal_code'),
        'place': data.get('place'),
        'birthday': data.get('birthday'),
        'phone': data.get('phone'),
        'email': data.get('email')
    }
    addresses.append(new_address)
    save_csv(addresses)

    return jsonify({"message": "Address added successfully!"}), 201


@app.route('/api/addresses/<int:id>', methods=['PUT'])
def update_address(id):
    data = request.json
    addresses = load_csv()

    # Find the address to update
    address = next((a for a in addresses if a['id'] == id), None)
    if not address:
        return jsonify({"error": "Address not found"}), 404

    # Update the relevant fields
    address.update({
        'firstname': data.get('firstname', address['firstname']),
        'lastname': data.get('lastname', address['lastname']),
        'street': data.get('street', address['street']),
        'number': data.get('number', address['number']),
        'postal_code': data.get('postal_code', address['postal_code']),
        'place': data.get('place', address['place']),
        'birthday': data.get('birthday', address['birthday']),
        'phone': data.get('phone', address['phone']),
        'email': data.get('email', address['email'])
    })

    save_csv(addresses)
    return jsonify({"message": "Address updated successfully!"})


@app.route('/api/addresses/<int:id>', methods=['DELETE'])
def delete_address(id):
    addresses = load_csv()

    # Find the address to delete
    address = next((a for a in addresses if a['id'] == id), None)
    if not address:
        return jsonify({"error": "Address not found"}), 404

    addresses.remove(address)
    save_csv(addresses)
    return jsonify({"message": "Address deleted successfully!"})


if __name__ == '__main__':
    app.run(debug=True)
