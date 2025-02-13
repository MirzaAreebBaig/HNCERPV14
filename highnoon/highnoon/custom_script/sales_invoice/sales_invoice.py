from __future__ import unicode_literals
#from frappe.model.document import Document
import frappe
from frappe import _
from datetime import date
from datetime import datetime # from python std library
from frappe.utils import add_to_date
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
            q = add_to_date(doc.start_date1, days=1)
            
            # Check if there is any record with the given criteria
            if frappe.db.exists("Sales Invoice", {"end_date1": doc.start_date1, "employee_name": doc.employee_name}):
                # Fetch details of the existing record to check its submission status
                existing_invoices = frappe.get_all(
                    "Sales Invoice",
                    filters={"end_date1": doc.start_date1, "employee_name": doc.employee_name},
                    fields=["docstatus"]
                )
                
                # Check if any fetched record is submitted
                for invoice in existing_invoices:
                    if invoice.docstatus == 1:
                        frappe.throw(frappe._("Till ({0}) invoice is already generated for employee '{1}'. Please generate next invoice from date ({2}).").format(doc.start_date1, doc.employee_name, q))
                        return

# def before_save_validate(doc, method):
#     if doc.items:
#         for item in doc.items:
#             existing_invoice = frappe.db.sql("""
#                 SELECT si.name
#                 FROM `tabSales Invoice` si
#                 INNER JOIN `tabSales Invoice Item` sii ON si.name = sii.parent
#                 WHERE sii.item_name = %s
#                 AND si.docstatus = 1
#                 AND (
#                     (si.start_date1 <= %s AND si.end_date1 >= %s) OR
#                     (si.start_date1 <= %s AND si.end_date1 >= %s) OR
#                     (si.start_date1 >= %s AND si.end_date1 <= %s)
#                 )
#             """, (item.item_name, doc.start_date1, doc.start_date1, doc.end_date1, doc.end_date1, doc.start_date1, doc.end_date1))

#             if existing_invoice and not doc.amended_from:
#                 frappe.throw(frappe._("An Invoice already exists with overlapping dates for employee ({0}) between start date - {1} and end date - {2}").format(item.item_name, doc.start_date1, doc.end_date1))


	

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

	