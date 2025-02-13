import frappe
from frappe.utils import flt, date_diff, add_days, getdate

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 150},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 200},
        {"label": "Date", "fieldname": "attendance_date", "fieldtype": "Date", "width": 100},
        {"label": "Hours", "fieldname": "custom_hours", "fieldtype": "Float", "width": 100},
        {"label": "Timesheet ID as per Client", "fieldname": "custom_timesheet_id_as_per_client", "fieldtype": "Data", "width": 150}
    ]

def get_data(filters):
    conditions = "1 = 1"
    if filters.get("from_date"):
        conditions += " AND attendance_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " AND attendance_date <= %(to_date)s"
    if filters.get("employee"):
        conditions += " AND employee = %(employee)s"
    attendance_records = frappe.db.sql(f"""
        SELECT
            employee, employee_name, attendance_date, custom_hours, custom_timesheet_id_as_per_client
        FROM
            `tabAttendance`
        WHERE
            {conditions}
    """, filters, as_dict=1)
    return attendance_records

@frappe.whitelist()
def create_timesheets(from_date, to_date, employee=None):
    # Prepare filters for the SQL query
    filters = {"from_date": from_date, "to_date": to_date}
    if employee:
        filters["employee"] = employee
    # Fetch all attendance records in the given period for the specified employee(s)
    attendance_records = frappe.db.sql(f"""
        SELECT
            employee, attendance_date, SUM(custom_hours) as total_hours, custom_timesheet_id_as_per_client
        FROM
            `tabAttendance`
        WHERE
            attendance_date BETWEEN %(from_date)s AND %(to_date)s
            {f"AND employee = %(employee)s" if employee else ""}
        GROUP BY
            employee, attendance_date, custom_timesheet_id_as_per_client
    """, filters, as_dict=1)
    # Group records by employee
    employee_records = {}
    for record in attendance_records:
        emp = record['employee']
        if emp not in employee_records:
            employee_records[emp] = []
        employee_records[emp].append(record)
    # Create timesheets for each employee
    for emp, records in employee_records.items():
        time_logs = []
        for record in records:
            time_logs.append({
                "activity_type": "Attendance",
                "from_time": f"{record['attendance_date']} 09:00:00",  # Adjust time as needed
                "hours": flt(record['total_hours']),
                "is_billable": True,
            })
        # Create the Timesheet document with custom_start_date, custom_end_date, and custom_fieldglass_ts_id
        timesheet = frappe.get_doc({
            "doctype": "Timesheet",
            "employee": emp,
            "custom_start_date": from_date,
            "custom_end_date": to_date,
            "custom_fieldglass_ts_id": records[0]['custom_timesheet_id_as_per_client'],  # Assuming one ID per timesheet
            "time_logs": time_logs
        })
        timesheet.insert()
        timesheet.save()
    return True
