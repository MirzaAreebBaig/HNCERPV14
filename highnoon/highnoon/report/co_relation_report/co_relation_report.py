# Copyright (c) 2022, 	kiran.c@indictrans.in and contributors
# For license information, please see license.txt

# import frappe


from __future__ import unicode_literals
from frappe import _ 
import frappe

def execute(filters=None):
	return get_columns(), get_data(filters)



def get_data(filters):
	_from, to = filters.get('from'), filters.get('to') #date range
	# conditions
	conditions = " AND 1=1 "
	if(filters.get('parent_cost_center')):conditions += f" AND parent_cost_center LIKE '%%{filters.get('parent_cost_center')}%%' "
	if(filters.get('child_center_name')):conditions += f" AND cost_center_name Like '%%{filters.get('child_center_name')}%%' "
	if(filters.get('customer')):conditions += f" AND customer='{filters.get('customer')}' "


	

	# data = frappe.db.sql(f"""select cc.parent_cost_center , cc.cost_center_name,s.customer,pe.start_date,pe.start_date, pe.end_date, pe.posting_date,ss.net_pay, s.posting_date, s.name, s.narration, s.total,p.reference_date ,(s.total - (0.1 * s.total)),(0.1 * s.total),s.due_date,(s.total - ss.net_pay ) from `tabCost Center` cc,`tabSales Invoice` s,`tabPayroll Entry` pe,`tabSalary Slip` ss,`tabPayment Entry`p where (pe.start_date between '{_from}' AND '{to}') {conditions} and cc.name= ss.payroll_cost_center and s.crrp  = p.crrp  and p.crrp  = pe.crrp and s.crrp = pe.crrp and pe.name= ss.payroll_entry and s.status != "Draft" and s.status != "Cancelled" and p.status = "Submitted" and ss.status = "Submitted" and cc.Disabled = "No";""")

	data = frappe.db.sql(f"""select cc.parent_cost_center , cc.cost_center_name,s.customer,pe.start_date,pe.start_date, pe.end_date, pe.posting_date,ss.net_pay, s.posting_date, s.name, s.narration, s.total,p.reference_date ,(s.total - (0.1 * s.total)),(0.1 * s.total),s.due_date,(s.total - ss.net_pay ) from `tabCost Center` cc,`tabSales Invoice` s,`tabPayroll Entry` pe,`tabSalary Slip` ss,`tabPayment Entry`p where (pe.start_date between '{_from}' AND '{to}') {conditions} and cc.name= ss.payroll_cost_center and s.cost_center  = p.cost_center  and p.cost_center  = ss.payroll_cost_center and s.cost_center = ss.payroll_cost_center and pe.name= ss.payroll_entry and s.status != "Draft" and s.status != "Cancelled" and p.status = "Submitted" and ss.status = "Submitted" and cc.Disabled = "No";""")
	
	

	

	return data

def get_columns():
	return [
		"Parent Cost Center:Link/Cost Center:180",
		"Child Cost Center:Data:180",
		"Customer:Data:150",
		"Service Month:Date:150",
		"Payroll Start Date:Date:150",
		"Payroll End Date:Date:150",
		"Salary Paid Date:Date:150",
		"Salary Amount Paid:Currency:150",
		"Invoice Date:Date:150",
		"Invoice Number:Link/Sales Invoice:150",
		"Invoice - Period:Data:200",
		"Invoice Amount:Currency:180",
		"Payment received Date:Date:180",
		"Invoice Payment received Amount:Currency:180",
		"TDS to be received:Currency:180",
		"Standard Receivable Date:Data:200",
		"Gross margin Amount:Currency:180",


		
		
	]
