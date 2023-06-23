import copy
from collections import OrderedDict

import frappe
from frappe import _, qb
from frappe.query_builder import CustomFunction
from frappe.query_builder.functions import Max
from frappe.utils import date_diff, flt, getdate




def execute(filters=None):
	""" columns, data = [], []
	return columns, data """
	if not filters:
		return [], [], None, []

	columns = get_columns(filters)
	conditions = get_conditions(filters)
	data =  get_data(filters,conditions)
	return columns, data,conditions, None   


def get_conditions(filters):
    conditions = ""
    if filters.get("from_date") and filters.get("to_date"):
        conditions += f" pe.start_date between '{filters.get('from_date')}' and '{filters.get('to_date')}'"
    if(filters.get('parent_cost_center')):conditions += f" AND parent_cost_center LIKE '%%{filters.get('parent_cost_center')}%%' "
    if(filters.get('child_center_name')):conditions += f" AND cost_center_name Like '%%{filters.get('child_center_name')}%%' "
    if(filters.get('customer')):conditions += f" AND customer='{filters.get('customer')}' "

	    
    return conditions     





def get_data(filters,conditions):
    

    data =frappe.db.sql(f"""SELECT 
	cc.parent_cost_center ,
	cc.cost_center_name,
	s.customer,
	pe.start_date,
	pe.start_date,
	pe.end_date,
	pe.posting_date,
	ss.net_pay,
	s.posting_date,
	s.name,
	s.narration,
	s.total,
	p.reference_date,
	(s.total - (0.1 * s.total)),
	(0.1 *s.total),
	s.due_date,
	(s.total - ss.net_pay )
	FROM `tabCost Center` cc
	LEFT JOIN `tabSales Invoice` s ON cc.name = s.cost_center
	LEFT JOIN `tabSalary Slip` ss ON cc.name = ss.payroll_cost_center
	LEFT JOIN `tabPayroll Entry` pe ON pe.name = ss.payroll_entry 
	LEFT JOIN `tabPayment Entry`p ON cc.name = p.cost_center
	WHERE {conditions}
	;
	""",as_dict=1,debug=1)
    return data
    
def get_columns(filters):
    columns = [
        {
            "label": _("Parent Cost Center"),
            "fieldname": "parent_cost_center",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": _("Child Cost Center"),
            "fieldname": "cost_center_name",
            "fieldtype": "Data",
            "width": 150,
        },
		{
            "label": _("Customer"),
            "fieldname": "customer",
            "fieldtype": "Data",
            "width": 150,
        },
		{
            "label": _("Service Month"),
            "fieldname": "start_date",
            "fieldtype": "Date",
            "width": 150,
        },
		{
            "label": _("Payroll Start Date"),
            "fieldname": "start_date",
            "fieldtype": "Date",
            "width": 150,
        },
		{
            "label": _("Payroll End Date"),
            "fieldname": "end_date",
            "fieldtype": "Date",
            "width": 150,
        },
		{
            "label": _("Salary Paid Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 150,
        },
		{
            "label": _("Salary Amount Paid"),
            "fieldname": "net_pay",
            "fieldtype": "Currency",
            "width": 150,
        },
		{
            "label": _("Invoice Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 150,
        },
		{
            "label": _("Invoice Number"),
            "fieldname": "name",
            "fieldtype": "Data",
            "width": 150,
        },
		{
            "label": _("Invoice - Period"),
            "fieldname": "narration",
            "fieldtype": "Data",
            "width": 150,
        },
		{
            "label": _("Invoice Amount"),
            "fieldname": "total",
            "fieldtype": "Currency",
            "width": 150,
        },
		{
            "label": _("Payment received Date"),
            "fieldname": "reference_date",
            "fieldtype": "Date",
            "width": 150,
        },
		{
            "label": _("Invoice Payment received Amount"),
            "fieldname": "(s.total - (0.1 * s.total))",
            "fieldtype": "Currency",
            "width": 150,
        },
		{
            "label": _("TDS to be received"),
            "fieldname": "(0.1 *s.total)",
            "fieldtype": "Currency",
            "width": 150,
        },
		{
            "label": _("Standard Receivable Date"),
            "fieldname": "due_date",
            "fieldtype": "Date",
            "width": 150,
        },
		{
            "label": _("Gross margin Amount"),
            "fieldname": "(s.total - ss.net_pay )",
            "fieldtype": "Currency",
            "width": 150,
        },
       
    ]
    return columns
	

