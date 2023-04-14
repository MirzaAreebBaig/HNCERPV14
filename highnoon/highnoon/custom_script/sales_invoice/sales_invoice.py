from __future__ import unicode_literals
#from frappe.model.document import Document
import frappe
from frappe import _
from frappe.utils import (
	now_datetime, getdate, formatdate
)

#-----------------------------
# def before_save(doc, method):
# 	if doc.item:
# 		customer_details = frappe.db.get_all('Item Customer Detail', filters={'parent': doc.item}, fields=['ref_code', 'work_order_date'], limit=1)
# 		print(customer_details)
# 		if customer_details:
# 			doc.po_no = customer_details[0]['ref_code']
# 			doc.po_date = customer_details[0]['work_order_date']


def before_save(doc, method):			
	if doc.items:
		for item in doc.items:
			if frappe.db.exists("Sales Invoice Item", {"item_name": item.item_name})  and frappe.db.exists("Sales Invoice", {"customer": doc.customer}) and frappe.db.exists("Sales Invoice", {"start_date1": doc.start_date1, "end_date1":doc.end_date1}) and not doc.amended_from and doc.is_new():
				frappe.throw(frappe._("An Customer Name ({1}) already exists with start date - {2} and end date - {3} and employee ({0})").format(item.item_name, doc.customer, doc.start_date1,doc.end_date1 ))

	

def validate_item_life(doc, method):
	end_of_life, disabled = frappe.db.get_value("Item", doc.item, ["end_of_life", "disabled"])

	if end_of_life and end_of_life != "0000-00-00" and getdate(end_of_life) <= now_datetime().date():
		frappe.throw(
			_("Item {0} has reached its end of life on {1}").format(doc.item, formatdate(end_of_life))
		)

	if disabled:
		frappe.throw(_("Item {0} is disabled").format(doc.item))


def validate_item_end_date(doc, method):
	item = doc.item
	valid_date = frappe.db.sql(""" select valid_upto from `tabItem Price` where item_code = %(item)s ORDER BY creation DESC LIMIT 1 """,{'item':item}, as_dict = 1)
	for i in valid_date:
		doc.item_date1 = i.valid_upto
		if str(doc.item_date1) < doc.end_date1:
			frappe.throw(frappe._("Item has been Expired. Last Date is {0}").format(formatdate(i.valid_upto)))

	