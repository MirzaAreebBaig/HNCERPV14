import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import (
	get_datetime,
)
@frappe.whitelist()
def mark_bulk_attendance(data):
    import json
    from frappe.utils import get_datetime

    # Ensure data is provided and not None
    if not data:
        frappe.throw(_("No data provided."))

    if isinstance(data, str):
        try:
            data = json.loads(data)  # Parse JSON data
        except json.JSONDecodeError:
            frappe.throw(_("Invalid JSON format."))

    data = frappe._dict(data)  # Convert to Frappe dict for easier access

    # Validate that 'unmarked_days' and 'employee' are present
    

    # Days of the week mapping, similar to the JS array
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Iterate through each date and create Attendance records
    for date_str in data.unmarked_days:
        if not date_str:
            continue  # Skip any empty or invalid dates
        
        # Convert date string to datetime object
        attendance_date = get_datetime(date_str)
        if not attendance_date:
            frappe.msgprint(_("Invalid date format: {0}").format(date_str))
            continue
        
        attendance_date = attendance_date.date()  # Get date part only

        # Calculate day of the week using the same logic as JS
        day_of_week = days_of_week[attendance_date.weekday()]
        frappe.log(day_of_week)

        # Check if attendance already exists for this employee and date
        if frappe.db.exists("Attendance", {
            "employee": data.employee,
            "attendance_date": attendance_date
        }):
            frappe.msgprint(_("Attendance for {0} on {1} already exists. Skipping.").format(data.employee, attendance_date))
            continue

        # Prepare the Attendance document
        doc_dict = {
            "doctype": "Attendance",
            "employee": data.employee,
            "attendance_date": attendance_date,
            "status": data.status,
            "custom_hours": data.get("custom_hours", 0),  # Default to 0 if not provided
            "custom_timesheet_id_as_per_client": data.get("custom_timesheet_id_as_per_client", ""),
            "custom_day": day_of_week  # Set the day of the week
        }

        # Create and save the Attendance document
        attendance = frappe.get_doc(doc_dict)
        attendance.insert(ignore_permissions=True)
        attendance.save()  # Automatically submits the document