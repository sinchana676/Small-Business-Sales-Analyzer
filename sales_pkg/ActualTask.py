
"""
Small Business Sales Analyzer - function definitions (package: sales_pkg).

A transaction is a dictionary:
{"day": "Mon", "item": "Tea", "quantity": 3, "price": 15.0}
"""

DAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")

# Product catalog: category -> {item: price in Rs.}
CATALOG = {
    "Beverages": {
        "Tea": 15,
        "Coffee": 20,
        "Cold Coffee": 45,
        "Lemon Juice": 25,
        "Milkshake": 60,
        "Mineral Water": 20,
    },
    "Snacks": {
        "Samosa": 12,
        "Veg Puff": 20,
        "French Fries": 50,
        "Sandwich": 40,
        "Vada Pav": 25,
        "Spring Roll": 45,
    },
    "Meals": {
        "Veg Biryani": 90,
        "Masala Dosa": 60,
        "Chole Bhature": 70,
        "Fried Rice": 80,
        "Veg Burger": 55,
    },
    "Desserts": {
        "Ice Cream": 35,
        "Brownie": 50,
        "Gulab Jamun": 30,
        "Cake Slice": 45,
    },
}


# Catalog helpers

def catalog_items():
    """Return the catalog as a flat list of (category, item, price)."""
    flat = []

    for category, products in CATALOG.items():
        for item, price in products.items():
            flat.append((category, item, price))

    return flat


def get_category(item):
    """Return the category of an item ('Other' if not found)."""
    for category, products in CATALOG.items():
        if item in products:
            return category

    return "Other"


def get_price(item):
    """Return catalog price. Raises ValueError if unknown."""
    for products in CATALOG.values():
        if item in products:
            return products[item]

    raise ValueError(f"'{item}' is not in the product catalog")


# Validation

def validate_transaction(transaction):
    """Check one transaction. Raises ValueError if invalid."""

    for key in ("day", "item", "quantity", "price"):
        if key not in transaction:
            raise ValueError(f"Missing field: {key}")

    if not isinstance(transaction["quantity"], int) or transaction["quantity"] <= 0:
        raise ValueError("Quantity must be a positive whole number")

    if not isinstance(transaction["price"], (int, float)) or transaction["price"] < 0:
        raise ValueError("Price cannot be negative")

    return True


def make_transaction(day, item, quantity):
    """Build a validated transaction using catalog price."""

    day = str(day).strip().capitalize()[:3]

    if day not in DAYS:
        raise ValueError("Day must be one of: " + ", ".join(DAYS))

    transaction = {
        "day": day,
        "item": item,
        "quantity": quantity,
        "price": get_price(item),
    }

    validate_transaction(transaction)

    return transaction


# Core analysis

def total_sales(transactions):
    """Return total sales amount of all transactions."""

    total = 0

    for t in transactions:
        validate_transaction(t)
        total += t["quantity"] * t["price"]

    return total


def best_seller(transactions):
    """Return (item, units_sold) of best-selling item, or None."""

    if not transactions:
        return None

    units = {}

    for t in transactions:
        validate_transaction(t)
        units[t["item"]] = units.get(t["item"], 0) + t["quantity"]

    top_item = max(units, key=units.get)

    return top_item, units[top_item]


def daily_average(transactions):
    """Return average sales per unique day."""

    if not transactions:
        raise ValueError("No transactions to analyze")

    days = set()

    for t in transactions:
        validate_transaction(t)
        days.add(t["day"])

    return total_sales(transactions) / len(days)


# Extra reports

def sales_by_item(transactions):
    """Return {item: (units_sold, revenue)}."""

    report = {}

    for t in transactions:
        validate_transaction(t)

        units, revenue = report.get(t["item"], (0, 0))

        report[t["item"]] = (
            units + t["quantity"],
            revenue + t["quantity"] * t["price"]
        )

    return report


def sales_by_category(transactions):
    """Return {category: revenue}."""

    report = {}

    for t in transactions:
        validate_transaction(t)

        cat = get_category(t["item"])

        report[cat] = (
            report.get(cat, 0) + t["quantity"] * t["price"]
        )

    return report


def sales_by_day(transactions):
    """Return {day: revenue}, ordered Monday to Sunday."""

    revenue = {}

    for t in transactions:
        validate_transaction(t)

        revenue[t["day"]] = (
            revenue.get(t["day"], 0) + t["quantity"] * t["price"]
        )

    return {d: revenue[d] for d in DAYS if d in revenue}


def best_day(transactions):
    """Return (day, revenue) of highest-earning day, or None."""

    daily = sales_by_day(transactions)

    if not daily:
        return None

    top = max(daily, key=daily.get)

    return top, daily[top]


def top_items(transactions, n=3):
    """Return top n items as a list of (item, units)."""

    if n <= 0:
        raise ValueError("n must be greater than zero")

    units = {
        item: data[0]
        for item, data in sales_by_item(transactions).items()
    }

    ranked = sorted(
        units.items(),
        key=lambda pair: pair[1],
        reverse=True
    )

    return ranked[:n]


def bill_with_gst(amount, gst_percent=5, discount_percent=0):
    """Return dict with discount, GST and final payable amount."""

    if amount < 0:
        raise ValueError("Amount cannot be negative")

    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100")

    if gst_percent < 0:
        raise ValueError("GST cannot be negative")

    discount = amount * discount_percent / 100
    taxable = amount - discount
    gst = taxable * gst_percent / 100

    return {
        "amount": amount,
        "discount": discount,
        "gst": gst,
        "payable": taxable + gst,
    }
