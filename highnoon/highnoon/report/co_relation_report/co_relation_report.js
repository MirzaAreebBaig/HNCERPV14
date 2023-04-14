// Copyright (c) 2022, 	kiran.c@indictrans.in and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Co-Relation Report"] = {
	"filters": [
	    {
			"fieldname":"parent_cost_center",
			"label": __("Parent Cost Center"),
			"fieldtype": "Data",
			"width": 100,
			"reqd":0,
		},
		{
			"fieldname":"child_center_name",
			"label": __("Child Center Name"),
			"fieldtype": "Data",
			"width": 100,
			"reqd":0,
		},
		{
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": 80,
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
		}

	]
};
