import frappe
from frappe.utils import nowdate
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    # Define columns for the report
    return [
        {"fieldname": "applicant_name", "label": _("Candidate Name"), "fieldtype": "Data", "width": 200},
        {"fieldname": "joining_date", "label": _("Date of Joining"), "fieldtype": "Date", "width": 120},
        {"fieldname": "resigned", "label": _("Resignation"), "fieldtype": "Check", "width": 100},
        {"fieldname": "resignation_accepted", "label": _("Resignation Accepted"), "fieldtype": "Check", "width": 100},
        {"fieldname": "relocated__at_work_location", "label": _("Relocation"), "fieldtype": "Select", "width": 100},
        {"fieldname": "bgv_ir_cleared", "label": _("BGV IR"), "fieldtype": "Check", "width": 100},
        {"fieldname": "last_working_date", "label": _("Last Working Date"), "fieldtype": "Date", "width": 120},
        {"fieldname": "source", "label": _("Source"), "fieldtype": "Data", "width": 100},
        {"fieldname": "additional_comments", "label": _("Comments"), "fieldtype": "Small Text", "width": 250}
    ]

def get_data(filters):
    # Ensure filters are present
    if not filters:
        filters = {}

    # Use provided dates or include all records if no filters are provided
    start_date = filters.get("start_date")
    end_date = filters.get("end_date")

    if start_date and end_date:
        # Filter records based on the date range
        query = """
            SELECT
                applicant_name, 
                joining_date, 
                resigned, 
                resignation_accepted, 
                relocated__at_work_location, 
                bgv_ir_cleared, 
                last_working_date,
                source,
                additional_comments 
            FROM `tabPre-Onboarding`
            WHERE joining_date BETWEEN %(start_date)s AND %(end_date)s
            ORDER BY creation DESC
        """
        return frappe.db.sql(query, {"start_date": start_date, "end_date": end_date}, as_dict=True)
    else:
        # Show all records if no date filters are provided
        query = """
            SELECT
                applicant_name, 
                joining_date, 
                resigned, 
                resignation_accepted, 
                relocated__at_work_location, 
                bgv_ir_cleared, 
                last_working_date,
                source,
                additional_comments 
            FROM `tabPre-Onboarding`
            ORDER BY creation DESC
        """
        return frappe.db.sql(query, as_dict=True)
