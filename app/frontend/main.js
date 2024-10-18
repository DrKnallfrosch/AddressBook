new Vue({
    el: '#app',
    data: {
        addresses: [],
        newAddress: {
            firstname: '',
            lastname: '',
            street: '',
            number: '',
            postal_code: '',
            place: '',
            birthday: '',
            phone: '',
            email: ''
        }
    },
    methods: {
        fetchAddresses() {
            fetch('http://127.0.0.1:5000/api/addresses')
                .then(response => response.json())
                .then(data => {
                    this.addresses = data;
                })
                .catch(error => {
                    console.error('Error fetching addresses:', error);
                });
        },
        addAddress() {
            fetch('http://127.0.0.1:5000/api/addresses', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.newAddress)
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                this.fetchAddresses();  // Refresh the list
            })
            .catch(error => {
                console.error('Error adding address:', error);
            });
        },
        deleteAddress(id) {
            fetch(`http://127.0.0.1:5000/api/addresses/${id}`, {
                method: 'DELETE'
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                this.fetchAddresses();  // Refresh the list
            })
            .catch(error => {
                console.error('Error deleting address:', error);
            });
        }
    }
});
