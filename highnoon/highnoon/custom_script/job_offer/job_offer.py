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

@frappe.whitelist()
def create_pre_onboarding_record(job_offer, applicant_name, joining_date, job_applicant):
    # Check if a Pre-Onboarding record already exists for this Job Offer
    if frappe.db.exists("Pre-Onboarding", {"job_offer": job_offer}):
        frappe.msgprint(_("A Pre-Onboarding record already exists for this Job Offer."), alert=True)
        return False

    # Fetch Job Applicant linked to this Job Offer
    job_applicant_doc = frappe.get_doc("Job Applicant", job_applicant)

    # Fetch the source field from the Job Applicant document
    source = job_applicant_doc.source

    # Create new Pre-Onboarding record
    pre_onboarding = frappe.get_doc({
        "doctype": "Pre-Onboarding",
        "job_offer": job_offer,
        "applicant_name": applicant_name,
        "joining_date": joining_date,
        "source": source,  # Insert the source value into the source field
        # Add any additional fields as needed
    })

    # Insert the new record
    pre_onboarding.insert(ignore_permissions=True)
    frappe.db.commit()  # Commit to ensure the record is saved

    # Check if the source field is set
    if source:
        # Fetch the Job Applicant Source document
        job_applicant_source = frappe.get_doc("Job Applicant Source", source)
        custom_source_mail = job_applicant_source.custom_source_mail

        if custom_source_mail:
            # Share the Pre-Onboarding document with custom_source_mail
            frappe.share.add_docshare("Pre-Onboarding", pre_onboarding.name, custom_source_mail, 1, 1, flags={"ignore_share_permission": True})

            # Assign the Pre-Onboarding document to custom_source_mail
            frappe.get_doc({
                "doctype": "ToDo",
                "allocated_to": custom_source_mail,
                "reference_type": "Pre-Onboarding",
                "reference_name": pre_onboarding.name,
                "description": "Please review and complete the Pre-Onboarding process."
            }).insert(ignore_permissions=True)

    return True
           
            


