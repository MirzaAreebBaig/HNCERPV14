import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data, None


def get_data(filters):
    if filters:
        _from, to = filters.get('from'), filters.get('to') 
        company = filters.get('company')
        data =frappe.db.sql(f"""SELECT 
        c.account_number,
        e.bank_ac_no,
        e.emp_name,
        s.net_pay,
        e.payment_mode,
        CAST(s.modified AS DATE) AS posting_date,
        e.ifsc_code,
        e.cell_number,
        e.personal_email
        FROM `tabCompany` c , `tabSalary Slip` s, `tabEmployee` e WHERE c.name = e.company and e.name = s.employee and (s.modified between '{_from}' AND '{to}') and e.company = %(company)s;
        """,{'company':company},as_dict=1,debug=1)
        return data
    else:
        data =frappe.db.sql(f"""SELECT 
        c.account_number,
        e.bank_ac_no,
        e.emp_name,
        s.net_pay,
        e.payment_mode,
        CAST(s.modified AS DATE) AS posting_date,
        e.ifsc_code,
        e.cell_number,
        e.personal_email
        FROM `tabCompany` c , `tabSalary Slip` s, `tabEmployee` e WHERE c.name = e.company and e.name = s.employee;
        """,as_dict=1,debug=1)
        return data    
    
def get_columns(filters):
	return  [
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
            "fieldname": "net_pay",
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
            "fieldtype": "Date",
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
            "fieldname": "credit_narration",
            "fieldtype": "Data",
            "width": 200,
        },
	
       
]
	

