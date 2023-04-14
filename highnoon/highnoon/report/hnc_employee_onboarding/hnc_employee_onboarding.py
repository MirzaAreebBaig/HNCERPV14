# Copyright (c) 2013, kiran and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
from frappe import _ 
import frappe

def execute(filters=None):
	return get_columns(), get_data(filters)


def get_data(filters):
	_from, to = filters.get('from'), filters.get('to') #date range
	# conditions
	conditions = " AND 1=1 "
	if(filters.get('name')):conditions += f" AND name LIKE '%%{filters.get('name')}%%' "
	if(filters.get('employee_name')):conditions += f" AND employee_name Like '%%{filters.get('employee_name')}%%' "
	if(filters.get('boarding_status')):conditions += f" AND boarding_status ='{filters.get('boarding_status')}' "

	data = frappe.db.sql(f"""select name,employee_name, date_of_joining, department, designation, boarding_status from `tabEmployee Onboarding` where (creation between '{_from}' AND '{to}') {conditions};""")
		

	return data
	
		

def get_columns():
	
	columns = [
        {
            "label": _("ID"),
            "fieldname": "name",
            "fieldtype": "Link",
			"options":"Employee Onboarding",
            "width": 150,
        },
        {
            "label": _("Employee Name"),
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": _("Date Of Joining"),
            "fieldname": "date_of_joining",
            "fieldtype": "Date",
            "width": 200,
        },
        {
            "label": _("Departmet"),
            "fieldname": "department",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "label": _("Designation"),
            "fieldname": "designation",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": _("Status"),
            "fieldname": "boarding_status",
            "fieldtype": "Data",
            "width": 150,
        },
]
	return columns
