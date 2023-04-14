import frappe

def get_dashboard_data(data):
    if 'Candidate' in frappe.get_roles(frappe.session.user) or 'ZHD-TAT' in frappe.get_roles(frappe.session.user):
        return {
            "fieldname": "job_applicant",
            "transactions": [
                {"items": ["Employee", "Employee Onboarding"]},
                {"items": ["Appointment Letter"]},
                {"items": ["Interview"]},
            ],
        }
    else:
        return {
		"fieldname": "job_applicant",
		"transactions": [
			{"items": ["Employee", "Employee Onboarding"]},
			{"items": ["Job Offer", "Appointment Letter"]},
			{"items": ["Interview"]},
		],
	}

def send_workflow_action_notification(doc, method):
    if doc.workflow_state == 'Pending for Approval':
        notification = frappe.get_doc('Notification', 'Job Applicant Approval')
     
        args={'doc': doc}

        recipients, cc, bb = notification.get_list_of_recipients(doc, args)

        frappe.enqueue(method=frappe.sendmail, recipients=[doc.cam_manager], sender=None, now=True,
            subject=frappe.render_template(notification.subject, args), message=frappe.render_template(notification.message, args))

    elif doc.workflow_state == 'Approved by CAM':
        notification = frappe.get_doc('Notification', 'Job Applicant Workflow Status')
     
        args={'doc': doc}

        recipients, cc, bb = notification.get_list_of_recipients(doc, args)

        frappe.enqueue(method=frappe.sendmail, recipients=recipients, sender=None, now=True,
            subject=frappe.render_template(notification.subject, args), message=frappe.render_template(notification.message, args))

    elif doc.workflow_state == 'Rejected by CAM':
        notification = frappe.get_doc('Notification', 'Job Applicant Workflow Status')
     
        args={'doc': doc}

        recipients, cc, bb = notification.get_list_of_recipients(doc, args)

        frappe.enqueue(method=frappe.sendmail, recipients=recipients, sender=None, now=True,
            subject=frappe.render_template(notification.subject, args), message=frappe.render_template(notification.message, args))



def validate_job_offer_joining_date(doc,method):
    name = frappe.db.get_all("Job Offer", filters = {"job_applicant":doc.name}, fields =["name"])
    if name:
        for i in name:
            frappe.db.set_value("Job Offer", i["name"] ,"joining_date" , doc.date_of_joining)
            frappe.db.set_value("Job Offer", i["name"] ,"applicant_name" , doc.applicant_name)
            frappe.db.set_value("Job Offer", i["name"] ,"applicant_father_name" , doc.applicant_father_name)
            frappe.db.set_value("Job Offer", i["name"] ,"salutation" , doc.salutation)
            frappe.db.set_value("Job Offer", i["name"] ,"applicant_email" , doc.email_id)
            frappe.db.set_value("Job Offer", i["name"] ,"phone_number" , doc.phone_number)
            frappe.db.set_value("Job Offer", i["name"] ,"country" , doc.country)
            frappe.db.set_value("Job Offer", i["name"] ,"gender" , doc.gender)
            frappe.db.set_value("Job Offer", i["name"] ,"job_title" , doc.job_title)
            frappe.db.set_value("Job Offer", i["name"] ,"designation" , doc.designation)
            frappe.db.set_value("Job Offer", i["name"] ,"address" , doc.address)
            frappe.db.set_value("Job Offer", i["name"] ,"cost_center" , doc.cost_center)
            frappe.db.set_value("Job Offer", i["name"] ,"currency" , doc.currency)
            frappe.db.set_value("Job Offer", i["name"] ,"ectc" , doc.upper_range)
            frappe.db.set_value("Job Offer", i["name"] ,"customer" , doc.client_name)
            frappe.db.set_value("Job Offer", i["name"] ,"company" , doc.company_name)
            frappe.db.set_value("Job Offer", i["name"] ,"deployment_location" , doc.deployment_location)
            frappe.db.set_value("Job Offer", i["name"] ,"primary_skill" , doc.primay_skill)
            frappe.db.set_value("Job Offer", i["name"] ,"secondary_skill" , doc.secondary_skill)
            frappe.db.set_value("Job Offer", i["name"] ,"aadhar_card" , doc.aadhar_card)
            frappe.db.set_value("Job Offer", i["name"] ,"pan_card" , doc.pan_card)
            frappe.db.set_value("Job Offer", i["name"] ,"pf_required" , doc.pf)
            frappe.db.commit()

def validate_employee_onboarding_joining_date(doc,method):
    name = frappe.db.get_all("Employee Onboarding", filters = {"job_applicant":doc.name}, fields =["name"])
    if name:
        for i in name:
            frappe.db.set_value("Employee Onboarding", i["name"] ,"date_of_joining" , doc.date_of_joining)
            frappe.db.set_value("Employee Onboarding", i["name"] ,"employee_name" , doc.applicant_name)
            frappe.db.set_value("Employee Onboarding", i["name"] ,"salutation" , doc.salutation)
            frappe.db.set_value("Employee Onboarding", i["name"] ,"email_id" , doc.email_id)
            frappe.db.set_value("Employee Onboarding", i["name"] ,"applicant_email_address" , doc.email_id)
            frappe.db.set_value("Employee Onboarding", i["name"] ,"designation" , doc.designation)
            frappe.db.set_value("Employee Onboarding", i["name"] ,"cost_center" , doc.cost_center)
            frappe.db.set_value("Employee Onboarding", i["name"] ,"client_name" , doc.client_name)
            frappe.db.set_value("Employee Onboarding", i["name"] ,"company" , doc.company_name)
            frappe.db.set_value("Employee Onboarding", i["name"] ,"deployment_location" , doc.deployment_location)
            frappe.db.set_value("Employee Onboarding", i["name"] ,"aadhar_card" , doc.aadhar_card)
            frappe.db.set_value("Employee Onboarding", i["name"] ,"pan_card" , doc.pan_card)
            frappe.db.commit()

def validate_employee_joining_date(doc,method):
    name = frappe.db.get_all("Employee", filters = {"job_applicant":doc.name}, fields =["name"])
    if name:
        for i in name:
            frappe.db.set_value("Employee", i["name"] ,"date_of_joining" , doc.date_of_joining)
            frappe.db.set_value("Employee", i["name"] ,"first_name" , doc.applicant_name)
            frappe.db.set_value("Employee", i["name"] ,"employee_name" , doc.applicant_name)
            frappe.db.set_value("Employee", i["name"] ,"applicant_father_name" , doc.applicant_father_name)
            frappe.db.set_value("Employee", i["name"] ,"salutation" , doc.salutation)
            frappe.db.set_value("Employee", i["name"] ,"email_id" , doc.email_id)
            frappe.db.set_value("Employee", i["name"] ,"cell_number" , doc.phone_number)
            frappe.db.set_value("Employee", i["name"] ,"country" , doc.country)
            frappe.db.set_value("Employee", i["name"] ,"gender" , doc.gender)
            frappe.db.set_value("Employee", i["name"] ,"job_opening" , doc.job_title)
            frappe.db.set_value("Employee", i["name"] ,"designation" , doc.designation)
            frappe.db.set_value("Employee", i["name"] ,"address" , doc.address)
            frappe.db.set_value("Employee", i["name"] ,"cost_center" , doc.cost_center)
            frappe.db.set_value("Employee", i["name"] ,"currency" , doc.currency)
            frappe.db.set_value("Employee", i["name"] ,"ectc" , doc.upper_range)
            frappe.db.set_value("Employee", i["name"] ,"customer" , doc.client_name)
            frappe.db.set_value("Employee", i["name"] ,"company" , doc.company_name)
            frappe.db.set_value("Employee", i["name"] ,"deployment_location" , doc.deployment_location)
            frappe.db.set_value("Employee", i["name"] ,"primary_skill" , doc.primay_skill)
            frappe.db.set_value("Employee", i["name"] ,"secondary_skill" , doc.secondary_skill)
            frappe.db.set_value("Employee", i["name"] ,"aadhar_number" , doc.aadhar_card)
            frappe.db.set_value("Employee", i["name"] ,"pan_number" , doc.pan_card)
            frappe.db.set_value("Employee", i["name"] ,"provident_fund" , doc.pf)
            frappe.db.set_value("Employee", i["name"] ,"client_name" , doc.client_name1)
            frappe.db.set_value("Employee", i["name"] ,"client_email_id" , doc.client_email_id)


            frappe.db.commit()

#---------------------Item doctype--------------------
def validate_item_joining_date(doc,method):
    name = frappe.db.get_all("Item", filters = {"job_applicant":doc.name}, fields =["name"])
    if name:
        for i in name:
            frappe.db.set_value("Item", i["name"] ,"full_name" , doc.applicant_name)
            frappe.db.set_value("Item", i["name"] ,"email_id" , doc.email_id)
            frappe.db.set_value("Item", i["name"] ,"cost_center" , doc.cost_center)
            frappe.db.set_value("Item", i["name"] ,"customer_master" , doc.client_name)
            frappe.db.set_value("Item", i["name"] ,"company" , doc.company_name)
            frappe.db.set_value("Item", i["name"] ,"deployment_location" , doc.deployment_location)
            frappe.db.set_value("Item", i["name"] ,"aadhar_card" , doc.aadhar_card)
            frappe.db.set_value("Item", i["name"] ,"pan_card" , doc.pan_card)
            frappe.db.commit()

def validate_sales_invoice_joining_date(doc,method):
    name = frappe.db.get_all("Sales Invoice", filters = {"job_applicant":doc.name}, fields =["name"])
    if name:
        for i in name:
            frappe.db.set_value("Sales Invoice", i["name"] ,"employee_name" , doc.applicant_name)
            frappe.db.set_value("Sales Invoice", i["name"] ,"email_id" , doc.email_id)
            frappe.db.set_value("Sales Invoice", i["name"] ,"cost_center" , doc.cost_center)
            frappe.db.set_value("Sales Invoice", i["name"] ,"customer" , doc.client_name)
            frappe.db.set_value("Sales Invoice", i["name"] ,"company" , doc.company_name)
            frappe.db.set_value("Sales Invoice", i["name"] ,"deployment_location" , doc.deployment_location)
            # frappe.db.set_value("Sales Invoice", i["name"] ,"aadhar_card" , doc.aadhar_card)
            # frappe.db.set_value("Sales Invoice", i["name"] ,"pan_card" , doc.pan_card)
            frappe.db.commit()            
            




