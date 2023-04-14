// Copyright (c) 2023, 	kiran.c@indictrans.in and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["HNC Employee Onboarding"] = {
	"filters": [
		{
			"fieldname":"name",
			"label": __("Name"),
			"fieldtype": "Data",
			"width": 100,
			"reqd":0,
		},
		{
			"fieldname":"employee_name",
			"label": __("Employee Name"),
			"fieldtype": "Data",
			"width": 150,
			"reqd":0,
			
		},
		{
			"fieldname":"boarding_status",
			"label": __("Status"),
			"fieldtype": "Select",
			"default": "",
			"options": ['','Pending', 'In Process', 'Completed'],
			"width": 100,
			"reqd":0,
		},
		{
			"fieldname":"from",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": 80,
			"reqd":1,
			"default": dateutil.year_start()
		},
		{
			"fieldname":"to",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": 80,
			"reqd":1,
			"default": dateutil.year_end()
		},

	]
};
