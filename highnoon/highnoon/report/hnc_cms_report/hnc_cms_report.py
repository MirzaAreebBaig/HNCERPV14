import json
import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data


def get_data(filters):
    if isinstance(filters, str):
        filters = json.loads(filters)

    date_filter = ""
    company = None

    if filters:
        _from, to = filters.get('start_date'), filters.get('end_date') 
        company = filters.get('company')
        
        if _from:
            date_filter += f"AND s.start_date >= '{frappe.utils.data.getdate(_from)}'"
        if to:
            date_filter += f" AND s.start_date <= '{frappe.utils.data.getdate(to)}'"

    if company:
        data = frappe.db.sql(f"""SELECT 
            c.account_number,
            e.bank_ac_no,
            e.emp_name,
            s.rounded_total,
            e.payment_mode,
            DATE_FORMAT(s.posting_date, '%%d-%%b-%%Y') AS posting_date,
            e.ifsc_code,
            e.cell_number,
            e.personal_email,
            CONCAT(
                'Salary credited for ',
                MONTHNAME(s.start_date),
                ' ',
                YEAR(s.start_date),
                ' from ',
                c.abbr
            ) AS custom_credit_narration
        FROM `tabCompany` c
        JOIN `tabEmployee` e ON c.name = e.company
        JOIN `tabSalary Slip` s ON e.name = s.employee
        WHERE e.company = %(company)s
        {date_filter};
        """, {'company': company}, as_dict=1)
    else:
        data = frappe.db.sql(f"""SELECT 
            c.account_number,
            e.bank_ac_no,
            e.emp_name,
            s.rounded_total,
            e.payment_mode,
            DATE_FORMAT(s.posting_date, '%d-%b-%Y') AS posting_date,
            e.ifsc_code,
            e.cell_number,
            e.personal_email,
            CONCAT(
                'Salary credited for ',
                MONTHNAME(s.start_date),
                ' ',
                YEAR(s.start_date),
                ' from ',
                c.abbr
            ) AS custom_credit_narration
        FROM `tabCompany` c
        JOIN `tabEmployee` e ON c.name = e.company
        JOIN `tabSalary Slip` s ON e.name = s.employee
        {date_filter};
        """, as_dict=1)

    return data


def get_columns(filters):
    return [
        {
            "label": _("From A/C No."),
            "fieldname": "account_number",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": _("A/C No."),
            "fieldname": "bank_ac_no",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": _("Beneficiary Name"),
            "fieldname": "emp_name",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": _("Amount"),
            "fieldname": "rounded_total",
            "fieldtype": "Currency",
            "width": 150,
        },
        {
            "label": _("Payment Mode"),
            "fieldname": "payment_mode",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": _("Posting Date"),
            "fieldname": "posting_date",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": _("IFSC Code"),
            "fieldname": "ifsc_code",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": _("Mobile Number"),
            "fieldname": "cell_number",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": _("Email Id"),
            "fieldname": "personal_email",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": _("Credit Narration"),
            "fieldname": "custom_credit_narration",
            "fieldtype": "Data",
            "width": 200,
        }
    ]


@frappe.whitelist()
def export_report_to_json(filters):
    columns, data = execute(filters)

    # Convert to JSON format
    result = {'columns': columns, 'data': data}
    json_data = json.dumps(result, default=str)

    return json_data