import frappe
from frappe.utils import flt, nowdate

@frappe.whitelist()
def get_projectwise_timesheet_data(project=None, parent=None, from_time=None, to_time=None, employee=None):
    condition = ""
    
    # Check if project filter is applied
    if project:
        condition += "AND tsd.project = %(project)s "
        
    # Check if parent filter (timesheet ID) is applied
    if parent:
        condition += "AND tsd.parent = %(parent)s "
        
    # Check if from_time and to_time filters are applied
    if from_time and to_time:
        condition += "AND CAST(tsd.from_time as DATE) BETWEEN %(from_time)s AND %(to_time)s"
        
    # Check if employee filter is applied
    if employee:
        condition += "AND ts.employee = %(employee)s "

    query = f"""
        SELECT
            tsd.name as name,
            tsd.parent as time_sheet,
            tsd.from_time as from_time,
            tsd.to_time as to_time,
            tsd.billing_hours as billing_hours,
            tsd.billing_amount as billing_amount,
            tsd.activity_type as activity_type,
            tsd.description as description,
            ts.currency as currency,
            tsd.project_name as project_name
        FROM `tabTimesheet Detail` tsd
            INNER JOIN `tabTimesheet` ts
            ON ts.name = tsd.parent
        WHERE
            tsd.parenttype = 'Timesheet'
            AND tsd.docstatus = 1
            AND tsd.is_billable = 1
            AND tsd.sales_invoice is NULL
            {condition}
        ORDER BY tsd.from_time ASC
    """

    filters = {
        "project": project,
        "parent": parent,
        "from_time": from_time,
        "to_time": to_time,
        "employee": employee
    }

    return frappe.db.sql(query, filters, as_dict=1)
