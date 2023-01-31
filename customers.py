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

    def __repr__(self):
        return (
            f"<Customer: {self.first_name} {self.last_name} || {self.email} >"
        )


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
    
    Parameters:
    email (str): Customer's email

    Returns:
    Customer obj    
    """

    return customers[email]


# Create dictionary of all customers from customer.txt
customers = read_customers_from_file("customers.txt")