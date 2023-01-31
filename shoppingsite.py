"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken, Katie Byers.
"""

from flask import Flask, render_template, redirect, flash, session, request
import jinja2

import melons
import customers

app = Flask(__name__)

# A secret key is needed to use Flask sessioning features
app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.
app.jinja_env.undefined = jinja2.StrictUndefined

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    print(melon)
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Melon successfully added to
    cart'."""

    # Create cart if it doesn't already exist in session
    if "cart" not in session:
        session["cart"] = {}

    print("Printing existing cart", session["cart"])

    # Increase melon quantity in cart by 1 (create melon in cart if doesn't already exist)
    session["cart"][melon_id] = session["cart"].get(melon_id, 0) + 1

    # Flash confirmation msg for user
    flash(f"Successfully added 1 melon ({melon_id}) to cart!")

    print("Printing updated cart", session["cart"])

    # Redirect user to cart page
    return redirect("/cart")


@app.route("/cart")
def show_shopping_cart():
    """Display content of shopping cart."""

    # Get the cart dictionary from the session
    cart = session.get("cart")

    order_contents = []
    order_total = 0

    # If cart is empty, flash msg
    if not cart:
        flash("Your cart is currently empty. Why don't you peruse our melon selection?")
    else:
        # Loop through each melon in cart
        for melon_id in cart:
            # Get melon obj
            melon = melons.get_by_id(melon_id)
            # Store qty as attribute
            melon.qty = cart[melon_id]
            # Calculate total cost and store as attribute
            melon.total_cost = melon.price * melon.qty

            # Add melon obj to order_contents list
            order_contents.append(melon)
            # Increase order total
            order_total += melon.total_cost

            print("Printing cart info")
            print("Current melon", melon)
            print(melon.qty)
            print(melon.total_cost)
            print("Current order contents", order_contents)
            print("Current order total", order_total)

    return render_template("cart.html",
        order_contents=order_contents,
        order_total=order_total)


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    email = request.form['email']
    password = request.form['password']

    print(email)
    print(password)

    # Retrieve customer with matching email (if any, otherwise will be None)
    customer = customers.get_by_email(email)

    # Check if customer with email exists
    if customer:
        # Check if provided password matches corresponding password
        if password == customer.password:
            # If passwords match, store user's email in session
            session["email"] = email
            # Flash success msg
            flash(f"Welcome back, {customer.first_name} {customer.last_name}! You are now logged in.")
            return redirect("/melons")

        # If passwords don't match
        else:
            # Flash error msg
            flash("Incorrect password. Please try again.")
    
    # If no matching email found, flash error msg
    else:
        flash("No customer with that email found. Please try again.")

    return redirect("/login")


@app.route("/logout")
def process_logout():
    """Log user out of site.

    Remove "email" from session dictionary.
    """
    session.pop("email")

    flash("You are now logged out.")
    return redirect("/melons")


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
