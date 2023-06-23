
__version__ = '0.0.1'

from hrms.hr.doctype.employee_onboarding.employee_onboarding import EmployeeOnboarding
from frappe.custom.doctype.customize_form.customize_form import (CustomizeForm
)
import frappe
from frappe import _

def validate_duplicate_employee_onboarding(self):
    emp_onboarding = frappe.db.exists("Employee Onboarding", {"job_applicant": self.job_applicant, 'docstatus': 1})
    if emp_onboarding and emp_onboarding != self.name:
        frappe.throw(
            _("Employee Onboarding: {0} is already for Job Applicant: {1}").format(
                frappe.bold(emp_onboarding), frappe.bold(self.job_applicant)
            )
        )

def allow_property_change(self, prop, meta_df, df):
    if prop == "fieldtype":
        self.validate_fieldtype_change(df, meta_df[0].get(prop), df.get(prop))

    elif prop == "length":
        old_value_length = cint(meta_df[0].get(prop))
        new_value_length = cint(df.get(prop))

        if new_value_length and (old_value_length > new_value_length):
            self.check_length_for_fieldtypes.append({"df": df, "old_value": meta_df[0].get(prop)})
            self.validate_fieldtype_length()
        else:
            self.flags.update_db = True

    elif prop == "allow_on_submit" and df.get(prop):
        if not frappe.db.get_value(
            "DocField", {"parent": self.doc_type, "fieldname": df.fieldname}, "allow_on_submit"
        ):
            frappe.msgprint(
                _("Row {0}: Not allowed to enable Allow on Submit for standard fields").format(df.idx)
            )
            return False

    # elif prop == "reqd" and (
    #     (
    #         frappe.db.get_value("DocField", {"parent": self.doc_type, "fieldname": df.fieldname}, "reqd")
    #         == 1
    #     )
    #     and (df.get(prop) == 0)
    # ):
    #     frappe.msgprint(
    #         _("Row {0}: Not allowed to disable Mandatory for standard fields").format(df.idx)
    #     )
    #     return False

    elif (
        prop == "in_list_view"
        and df.get(prop)
        and df.fieldtype != "Attach Image"
        and df.fieldtype in no_value_fields
    ):
        frappe.msgprint(
            _("'In List View' not allowed for type {0} in row {1}").format(df.fieldtype, df.idx)
        )
        return False

    elif (
        prop == "precision"
        and cint(df.get("precision")) > 6
        and cint(df.get("precision")) > cint(meta_df[0].get("precision"))
    ):
        self.flags.update_db = True

    elif prop == "unique":
        self.flags.update_db = True

    elif (
        prop == "read_only"
        # and cint(df.get("read_only")) == 0
        and frappe.db.get_value(
            "DocField", {"parent": self.doc_type, "fieldname": df.fieldname}, "read_only"
        )
        == 1
    ):
        # if docfield has read_only checked and user is trying to make it editable, don't allow it
        frappe.msgprint(_("You cannot unset 'Read Only' for field {0}").format(df.label))
        return False

    elif prop == "options" and df.get("fieldtype") not in ALLOWED_OPTIONS_CHANGE:
        frappe.msgprint(_("You can't set 'Options' for field {0}").format(df.label))
        return False

    elif prop == "translatable" and not supports_translation(df.get("fieldtype")):
        frappe.msgprint(_("You can't set 'Translatable' for field {0}").format(df.label))
        return False

    elif prop == "in_global_search" and df.in_global_search != meta_df[0].get("in_global_search"):
        self.flags.rebuild_doctype_for_global_search = True

    return True

doctype_properties = {
	"search_fields": "Data",
	"title_field": "Data",
	"image_field": "Data",
	"sort_field": "Data",
	"sort_order": "Data",
	"default_print_format": "Data",
	"allow_copy": "Check",
	"istable": "Check",
	"quick_entry": "Check",
	"editable_grid": "Check",
	"max_attachments": "Int",
	"make_attachments_public": "Check",
	"track_changes": "Check",
	"track_views": "Check",
	"allow_auto_repeat": "Check",
	"allow_import": "Check",
	"show_preview_popup": "Check",
	"default_email_template": "Data",
	"email_append_to": "Check",
	"subject_field": "Data",
	"sender_field": "Data",
	"autoname": "Data",
	"translated_doctype": "Check",
}

docfield_properties = {
	"idx": "Int",
	"label": "Data",
	"fieldtype": "Select",
	"options": "Text",
	"fetch_from": "Small Text",
	"fetch_if_empty": "Check",
	"permlevel": "Int",
	"width": "Data",
	"print_width": "Data",
	"non_negative": "Check",
	"reqd": "Check",
	"unique": "Check",
	"ignore_user_permissions": "Check",
	"in_list_view": "Check",
	"in_standard_filter": "Check",
	"in_global_search": "Check",
	"in_preview": "Check",
	"bold": "Check",
	"no_copy": "Check",
	"ignore_xss_filter": "Check",
	"hidden": "Check",
	"collapsible": "Check",
	"collapsible_depends_on": "Data",
	"print_hide": "Check",
	"print_hide_if_no_value": "Check",
	"report_hide": "Check",
	"allow_on_submit": "Check",
	"translatable": "Check",
	"mandatory_depends_on": "Data",
	"read_only_depends_on": "Data",
	"depends_on": "Data",
	"description": "Text",
	"default": "Text",
	"precision": "Select",
	"read_only": "Check",
	"length": "Int",
	"columns": "Int",
	"remember_last_selected_value": "Check",
	"allow_bulk_edit": "Check",
	"auto_repeat": "Link",
	"allow_in_quick_entry": "Check",
	"hide_border": "Check",
	"hide_days": "Check",
	"hide_seconds": "Check",
}

doctype_link_properties = {
	"link_doctype": "Link",
	"link_fieldname": "Data",
	"group": "Data",
	"hidden": "Check",
}

doctype_action_properties = {
	"label": "Link",
	"action_type": "Select",
	"action": "Small Text",
	"group": "Data",
	"hidden": "Check",
}


ALLOWED_FIELDTYPE_CHANGE = (
	("Currency", "Float", "Percent"),
	("Small Text", "Data"),
	("Text", "Data"),
	("Text", "Text Editor", "Code", "Signature", "HTML Editor"),
	("Data", "Select"),
	("Text", "Small Text"),
	("Text", "Data", "Barcode"),
	("Code", "Geolocation"),
	("Table", "Table MultiSelect"),
)

ALLOWED_OPTIONS_CHANGE = ("Read Only", "HTML", "Data")

EmployeeOnboarding.validate_duplicate_employee_onboarding = validate_duplicate_employee_onboarding
CustomizeForm.allow_property_change = allow_property_change