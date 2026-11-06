
import random

from sales_pkg import (
    catalog_items,
    make_transaction,
    total_sales,
    best_seller,
    daily_average,
    sales_by_item,
    sales_by_category,
    sales_by_day,
    best_day,
    top_items,
    bill_with_gst,
    DAYS,
)

sales = []  # Every sale recorded in this session


def line(char="-", width=50):
    print(char * width)


def show_catalog():
    print("\nPRODUCT MENU")
    line()
    current = None

    for number, (category, item, price) in enumerate(catalog_items(), start=1):
        if category != current:
            print(f"[{category}]")
            current = category

        print(f"  {number:>2}. {item:<15} Rs. {price}")


def record_sale():
    show_catalog()
    items = catalog_items()

    try:
        number = int(input("\nEnter item number: "))

        if not 1 <= number <= len(items):
            print("Error -> Item number is not in the menu.")
            return

        quantity = int(input("Quantity: "))

    except ValueError:
        print("Error -> Please enter whole numbers only.")
        return

    day = input("Day (Mon/Tue/Wed/Thu/Fri/Sat/Sun): ")

    try:
        sale = make_transaction(day, items[number - 1][1], quantity)

    except ValueError as e:
        print("Error ->", e)
        return

    sales.append(sale)

    print(
        f"Recorded: {sale['quantity']} x {sale['item']} "
        f"on {sale['day']} = "
        f"Rs. {sale['quantity'] * sale['price']:.2f}"
    )


def show_all_sales():
    if not sales:
        print("No sales recorded yet.")
        return

    line()
    print(f"{'No':<4}{'Day':<6}{'Item':<16}{'Qty':<5}{'Price':<8}{'Amount':<8}")
    line()

    for i, s in enumerate(sales, start=1):
        print(
            f"{i:<4}{s['day']:<6}{s['item']:<16}"
            f"{s['quantity']:<5}{s['price']:<8}"
            f"{s['quantity'] * s['price']:<8.2f}"
        )


def show_total_and_bill():
    total = total_sales(sales)

    print(f"Total sales : Rs. {total:.2f}")

    try:
        gst = float(input("GST % (press Enter for 5): ") or 5)
        disc = float(input("Discount % (press Enter for 0): ") or 0)

        bill = bill_with_gst(total, gst, disc)

    except ValueError as e:
        print("Error ->", e)
        return

    line()
    print(f"Amount      : Rs. {bill['amount']:.2f}")
    print(f"Discount    : Rs. {bill['discount']:.2f}")
    print(f"GST         : Rs. {bill['gst']:.2f}")
    print(f"Payable     : Rs. {bill['payable']:.2f}")


def show_best_sellers():
    result = best_seller(sales)

    if result is None:
        print("No sales recorded yet.")
        return

    print(f"Best seller: {result[0]} ({result[1]} units)")
    print("Top 3 items:")

    for rank, (item, units) in enumerate(top_items(sales, 3), start=1):
        print(f"  {rank}. {item:<15} {units} units")


def show_daily_stats():
    if not sales:
        print("No sales recorded yet.")
        return

    print(f"Daily average : Rs. {daily_average(sales):.2f}")

    day, amount = best_day(sales)

    print(f"Best day      : {day} (Rs. {amount:.2f})")


def show_category_report():
    if not sales:
        print("No sales recorded yet.")
        return

    total = total_sales(sales)

    for cat, amount in sorted(
        sales_by_category(sales).items(),
        key=lambda p: p[1],
        reverse=True
    ):
        print(
            f"{cat:<12} Rs. {amount:>8.2f} "
            f"({amount / total * 100:.1f}%)"
        )


def show_day_report():
    if not sales:
        print("No sales recorded yet.")
        return

    for day, amount in sales_by_day(sales).items():
        print(
            f"{day:<5} Rs. {amount:>8.2f} "
            + "#" * int(amount // 50)
        )


def show_item_report():
    if not sales:
        print("No sales recorded yet.")
        return

    print(f"{'Item':<16}{'Units':<8}{'Revenue':<10}")
    line()

    report = sales_by_item(sales)

    for item, (units, revenue) in sorted(
        report.items(),
        key=lambda p: p[1][1],
        reverse=True
    ):
        print(f"{item:<16}{units:<8}Rs. {revenue:.2f}")


def load_sample_week():
    """Create a week of simulated sales (same data every time)."""

    random.seed(42)
    items = catalog_items()

    for day in DAYS:
        for _ in range(random.randint(6, 9)):
            item = random.choice(items)[1]
            sales.append(
                make_transaction(day, item, random.randint(1, 12))
            )

    print(f"Loaded {len(sales)} total sales in the session.")


def save_report():
    if not sales:
        print("No sales recorded yet.")
        return

    with open("sales_report.txt", "w") as f:
        f.write("SMALL BUSINESS SALES REPORT\n")
        f.write("=" * 30 + "\n")

        f.write(f"Total sales   : Rs. {total_sales(sales):.2f}\n")
        f.write(f"Daily average : Rs. {daily_average(sales):.2f}\n")

        item, units = best_seller(sales)
        f.write(f"Best seller   : {item} ({units} units)\n")

        day, amount = best_day(sales)
        f.write(f"Best day      : {day} (Rs. {amount:.2f})\n")

    print("Report saved to sales_report.txt")


def main():
    actions = {
        "1": record_sale,
        "2": show_catalog,
        "3": show_all_sales,
        "4": show_total_and_bill,
        "5": show_best_sellers,
        "6": show_daily_stats,
        "7": show_category_report,
        "8": show_day_report,
        "9": show_item_report,
        "10": load_sample_week,
        "11": save_report,
    }

    print("=" * 50)
    print("      SMALL BUSINESS SALES ANALYZER")
    print("=" * 50)

    while True:
        print("\n 1. Record a sale          7. Sales by category")
        print(" 2. Show product menu      8. Sales by day")
        print(" 3. Show all sales         9. Item-wise report")
        print(" 4. Total sales & bill    10. Load sample week")
        print(" 5. Best sellers          11. Save report to file")
        print(" 6. Daily average         0. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "0":
            print("Thank you!")
            break

        if choice in actions:
            print()
            actions[choice]()

        else:
            print("Invalid choice. Please select from the menu.")


if __name__ == "__main__":
    main()
