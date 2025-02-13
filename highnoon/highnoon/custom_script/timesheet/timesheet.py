import frappe
from frappe.utils import getdate

@frappe.whitelist()
def create_attendance_from_timesheets(timesheet_name=None):
    if not timesheet_name:
        frappe.throw(("Please provide a Timesheet name"))

    # Fetch the timesheet document
    timesheet = frappe.get_doc("Timesheet", timesheet_name)

    # Iterate over each time log in the timesheet
    for time_log in timesheet.time_logs:
        # Ensure the activity_type is "Attendance"
        if time_log.activity_type != "Attendance":
            continue

        # Extract the date from the from_time field
        attendance_date = getdate(time_log.from_time)

        # Create an attendance record for each day in the time log
        attendance = frappe.get_doc({
            "doctype": "Attendance",
            "employee": timesheet.employee,
            "attendance_date": attendance_date,
            "status": time_log.custom_status,  # Use the custom_status from the time log
            "custom_hours": time_log.hours,
            "company": timesheet.company
        })

        # Insert and submit the attendance record
        attendance.insert()
        attendance.save()

    return True

@frappe.whitelist()
def fetch_employee_item_and_calculate_discount(timesheet_id):
    """
    Fetch item for employee, calculate pricing rule based on item code, and update custom_rate field in Timesheet.
    """
    # Fetch timesheet details
    timesheet = frappe.get_doc("Timesheet", timesheet_id)

    # Get the employee from the timesheet
    employee = timesheet.employee

    # Fetch the item associated with the employee from the Item doctype
    item_code = frappe.db.get_value("Item", {"employee": employee}, "item_code")

    if not item_code:
        frappe.throw(f"No item associated with the employee {employee}")
    
    # Fetch the item price from Item Price doctype
    price_list_rate = frappe.db.get_value("Item Price", {"item_code": item_code}, "price_list_rate")

    if not price_list_rate:
        frappe.throw(f"No base price found for item {item_code} in the Item Price doctype")

    # Calculate pricing rule and discount
    discount_details = calculate_discount_for_item_code(item_code, price_list_rate)

    # Update the custom_rate field in the Timesheet
    discounted_rate = discount_details.get("discounted_rate")
    timesheet.custom_rate = discounted_rate

    return discount_details


def calculate_discount_for_item_code(item_code, price_list_rate):
    """
    Function to calculate the discount based on pricing rules for a given item code.
    :param item_code: The item code to calculate the discount for.
    :param price_list_rate: The base rate fetched from the Item Price doctype.
    :return: A dictionary with the discounted rate, price list rate, discount percentage, and discount amount.
    """
    
    price_list_rate_float = float(price_list_rate if price_list_rate is not None else 0)

    # Fetch pricing rules based on item code
    query_item_code = """
    SELECT pr.name, pr.discount_percentage, pr.min_amt, pr.min_qty, pr.rate_or_discount, pr.apply_on, pr.discount_amount, pr.rate
    FROM `tabPricing Rule` AS pr
    JOIN `tabPricing Rule Item Code` AS pric ON pric.parent = pr.name
    WHERE pric.item_code = %s
    """
    pricing_rules_on_item_code = frappe.db.sql(query_item_code, (item_code,), as_dict=True)

    if not pricing_rules_on_item_code:
        return {
            "discounted_rate": price_list_rate,
            "price_list_rate": price_list_rate,
            "discount_percentage": 0,
            "discount_amount": 0
        }

    # Initialize variables for calculating the final discounted rate
    final_discounted_rate = price_list_rate_float
    total_discount_amount = 0.0
    discount_percentage = 0.0

    for rule in pricing_rules_on_item_code:
        if rule["min_qty"] < 2:
            if rule["rate_or_discount"] == "Rate":
                new_rate_float = float(rule["rate"])
                final_discounted_rate = min(final_discounted_rate, new_rate_float)
            elif rule["rate_or_discount"] == "Discount Amount":
                discount_amount = float(rule["discount_amount"])
                final_discounted_rate = max(final_discounted_rate - discount_amount, 0)
                total_discount_amount += discount_amount
            elif rule["rate_or_discount"] == "Discount Percentage":
                discount_percentage = float(rule["discount_percentage"])
                discounted_rate = price_list_rate_float - (price_list_rate_float * (discount_percentage / 100.0))
                final_discounted_rate = min(final_discounted_rate, discounted_rate)
                total_discount_amount = price_list_rate_float - final_discounted_rate

    return {
        "discounted_rate": final_discounted_rate,
        "price_list_rate": price_list_rate,
        "discount_percentage": discount_percentage,
        "discount_amount": total_discount_amount
    }