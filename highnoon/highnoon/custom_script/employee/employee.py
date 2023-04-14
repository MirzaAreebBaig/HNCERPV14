from __future__ import unicode_literals
import frappe
from frappe.utils import today
from frappe.utils import date_diff
from frappe import _


def before_save(self, method):
    #calculation no. of days.
    today_date = today()
    joining_date = self.date_of_joining
    number_of_days = date_diff(today_date, joining_date)
    self.nos_of_days = number_of_days

    # calculation of PO or PM
    self.new_po_or_pm = self.po_per_month_

    # calculation of CTC OR Salary PM
    self.new_ctc_or_salary_pm = self.new_salary_per_month

    # calculation of Salary
    self.new_salary = ((self.new_ctc_or_salary_pm) * 12 /365 * (self.nos_of_days))

    # Calculation of Base
    self.new_base = ((self.new_po_or_pm) * 12 / 365 * (self.nos_of_days))

    # Calculation of GST
    self.gst = (self.new_base * 18/100)

    # Calculation of Total
    self.new_total = (self.new_base + self.gst)

    # Calculation of TDS
    self.new_tds = (self.new_base * 10/100)

    # Calculation of AF Tax
    self.new_af_tax = (self.new_total - self.new_tds)

    # Calculation of Amt in Bank or Profit
    self.new_amt_in_bank_or_profit = (self.new_af_tax - self.new_salary)

    # Calculation of Fixed Cost Margin or Net Profit
    self.new_fixed_cost_margin_or_net_profit = (self.new_amt_in_bank_or_profit -(self.new_amt_in_bank_or_profit * 10/100))

    # Calculation of 40 Percentage on Base
    self.new_percentage_on_base = (self.new_base *40/100)

    # Calculation of Below 40 Percentage
    self.new_below_40_percentage = (self.new_fixed_cost_margin_or_net_profit - self.new_percentage_on_base )

    # Calculation of Percentage
    self.new_percentage = ((self.new_fixed_cost_margin_or_net_profit) / (self.new_base) * 100)
    
    try:
        frappe.db.sql(""" 
                update 
                    tabItem 
                set    
                    customer_master = '{}', customer_address = '{}', full_address = '{}'
                where
                    employee = '{}'
                """.format(self.customer, self.customer_address1, self.full_address, self.name))
    except Exception:
        return
    frappe.db.commit()

@frappe.whitelist(allow_guest=True)
def get_customer_addresses(doctype, txt, searchfield, start, page_len, filters):
    address = frappe.db.sql(""" 
                select 
                    ads.name, ads.country, ads.state
                from
                    `tabAddress` as ads
                join
                    `tabDynamic Link` as dl
                on 
                    dl.parent = ads.name
                where
                    dl.link_doctype = 'Customer'
                    and dl.link_name = '{}'
                    and ads.disabled = 0
                """.format(filters['customer']))
    return address


def update_item_details(doc,method):
    name = frappe.db.get_all("Item", filters = {"employee":doc.name}, fields =["name"])
    if name:
        for i in name:
            frappe.db.set_value("Item", i["name"] ,"wo_po_id" , doc.work_order_number)
            frappe.db.set_value("Item", i["name"] ,"work_order_date" , doc.work_order_date)
            frappe.db.set_value("Item", i["name"] ,"new_billing" , doc.new_billing)
            frappe.db.set_value("Item", i["name"] ,"start_date" , doc.start_date)
            frappe.db.set_value("Item", i["name"] ,"end_date" , doc.end_date)
            frappe.db.set_value("Item", i["name"] ,"client_entity" , doc.client_entity)
            frappe.db.commit()

def update_sales_invoice_details(doc,method):
    name = frappe.db.get_all("Sales Invoice", filters = {"item":doc.name}, fields =["name"])
    if name:
        for i in name:
            frappe.db.set_value("Sales Invoice", i["name"] ,"po_no" , doc.work_order_number)
            frappe.db.set_value("Sales Invoice", i["name"] ,"po_date" , doc.work_order_date)
            frappe.db.set_value("Sales Invoice", i["name"] ,"new_billing" , doc.new_billing)
            frappe.db.set_value("Sales Invoice", i["name"] ,"item_date" , doc.end_date)
            frappe.db.set_value("Sales Invoice", i["name"] ,"client_entity" , doc.client_entity)
            frappe.db.commit()            
    