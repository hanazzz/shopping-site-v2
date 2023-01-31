"""Customers at Hackbright."""


class Customer:
    """Ubermelon customer."""

    def __init__(
        self,
        first_name,
        last_name,
        email,
        password,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.hashed_password = hash(password)

    def __repr__(self):
        return (
            f"<Customer: {self.first_name} {self.last_name} || {self.email} >"
        )

    def check_password(self, password):
        """Check if password is correct password for this customer.

        Compare the hash of password to the stored hash of the original password.

        Arguments:
        password (strO): User-provided password

        Returns:
        is_correct (bool): True if passwords match, False if not
        """

        is_correct = hash(password) == self.hashed_password

        return is_correct


def read_customers_from_file(filepath):
    """Read customer data and populate dictionary of customers.

    Parameters:
    filepath (str): Path to file with customer data

    Returns:
    customers (dict): Dictionary of customers ({email: Customer object})
    """

    customers = {}

    with open(filepath) as file:
        for line in file:
            # Remove any leading/trailing whitespace and split at "|"
            # Store resulting strings in corresponding vars
            (
                first_name,
                last_name,
                email,
                password
            ) = line.strip().split("|")

            # Create customer obj
            customer = Customer(first_name, last_name, email, password)

            # Add customer to dictionary
            customers[email] = customer

    return customers


def get_by_email(email):
    """Return a customer, given their email.
    
    Returns None if no customer with matching email is found.
    
    Parameters:
    email (str): Customer's email

    Returns:
    Customer obj    
    """

    return customers.get(email)


# Create dictionary of all customers from customer.txt
customers = read_customers_from_file("customers.txt")