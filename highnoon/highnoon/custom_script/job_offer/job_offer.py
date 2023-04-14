from __future__ import unicode_literals
import frappe
from frappe import _

def validate(doc, method):
    name = frappe.db.get_all("Job Applicant", filters = {"name":doc.job_applicant}, fields =["name"])
    if name:
        for i in name:
            if doc.docstatus == 0:
                frappe.db.set_value("Job Applicant", i["name"] ,"job_offer_status" ,"Draft")
                frappe.db.set_value("Job Applicant", i["name"] ,"job_offer_no" , doc.name)
                frappe.db.commit()
            elif doc.docstatus == 1:
                frappe.db.set_value("Job Applicant", i["name"] ,"job_offer_status" , doc.status)    
                frappe.db.set_value("Job Applicant", i["name"] ,"job_offer_no" , doc.name)
                frappe.db.commit()
            else:
                pass       
            
            


