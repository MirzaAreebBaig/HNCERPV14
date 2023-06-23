from . import __version__ as app_version

app_name = "highnoon"
app_title = "Highnoon"
app_publisher = "	kiran.c@indictrans.in"
app_description = "highnoon"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "kiran.c@indictrans.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/highnoon/css/highnoon.css"
# app_include_js = "/assets/highnoon/js/highnoon.js"

# include js, css files in header of web template
# web_include_css = "/assets/highnoon/css/highnoon.css"
# web_include_js = "/assets/highnoon/js/highnoon.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "highnoon/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page

# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Job Offer" : "highnoon/custom_script/job_offer/job_offer.js",
	"Job Applicant": "highnoon/custom_script/job_applicant/job_applicant.js",
	"Sales Invoice" : "highnoon/custom_script/sales_invoice/sales_invoice.js",
	"Payment Entry" : "highnoon/custom_script/payment_entry/payment_entry.js",
	"Employee" : "highnoon/custom_script/employee/employee.js",
	"Item" : "highnoon/custom_script/item/item.js",
	"Item Price" : "highnoon/custom_script/item_price/item_price.js"
	}

# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

doctype_list_js = {
	"Job Applicant": "highnoon/custom_script/job_applicant/job_applicant_list.js"
}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "highnoon.install.before_install"
# after_install = "highnoon.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "highnoon.uninstall.before_uninstall"
# after_uninstall = "highnoon.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "highnoon.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#e
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }
fixtures = ["Custom Field", "Property Setter", "Print Format", "Workflow", "Workflow State", "Workflow Action Master","Client Script"] 

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"Sales Invoice": "highnoon.highnoon.custom_script.sales_invoice.sales_invoice.SalesInvoice"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Sales Invoice":{
		"before_save":["highnoon.highnoon.custom_script.sales_invoice.sales_invoice.validate_item_end_date","highnoon.highnoon.custom_script.sales_invoice.sales_invoice.before_save","highnoon.highnoon.custom_script.sales_invoice.sales_invoice.before_save_validate"],
		"before_insert": "highnoon.highnoon.custom_script.sales_invoice.sales_invoice.validate_item_life"
		
	},
	"Employee":{
		"before_save":["highnoon.highnoon.custom_script.employee.employee.before_save",
		"highnoon.highnoon.custom_script.employee.employee.update_item_details",
		"highnoon.highnoon.custom_script.employee.employee.update_sales_invoice_details",
		"highnoon.highnoon.custom_script.employee.employee.update_job_offer_cost_center",
		"highnoon.highnoon.custom_script.employee.employee.update_job_applicant_cost_center"],
		"before_save":"highnoon.highnoon.custom_script.employee.employee.validate"
	},
	"Job Offer":{
		"before_save":"highnoon.highnoon.custom_script.job_offer.job_offer.validate",
		"on_submit":"highnoon.highnoon.custom_script.job_offer.job_offer.validate",
		"on_update_after_submit":"highnoon.highnoon.custom_script.job_offer.job_offer.validate"
	},
	"Job Applicant": {
		"on_change": "highnoon.highnoon.custom_script.job_applicant.job_applicant.send_workflow_action_notification",
		"before_save":["highnoon.highnoon.custom_script.job_applicant.job_applicant.validate_job_offer_joining_date","highnoon.highnoon.custom_script.job_applicant.job_applicant.validate_employee_onboarding_joining_date","highnoon.highnoon.custom_script.job_applicant.job_applicant.validate_employee_joining_date","highnoon.highnoon.custom_script.job_applicant.job_applicant.validate_item_joining_date","highnoon.highnoon.custom_script.job_applicant.job_applicant.validate_sales_invoice_joining_date","highnoon.highnoon.custom_script.job_applicant.job_applicant.pan_card_uniqueness"]

	}
	
	
	
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"highnoon.tasks.all"
#	],
#	"daily": [
#		"highnoon.tasks.daily"
#	],
#	"hourly": [
#		"highnoon.tasks.hourly"
#	],
#	"weekly": [
#		"highnoon.tasks.weekly"
#	]
#	"monthly": [
#		"highnoon.tasks.monthly"
#	]
# }

scheduler_events = {
	"daily": [
		"highnoon.highnoon.custom_script.item.item.send_notification_about_item_expiry"
	]
}

# Testing
# -------

# before_tests = "highnoon.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "highnoon.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "highnoon.task.get_dashboard_data"
# }

override_doctype_dashboards = {
	"Job Applicant": "highnoon.highnoon.custom_script.job_applicant.job_applicant.get_dashboard_data"
}

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"highnoon.auth.validate"
# ]

