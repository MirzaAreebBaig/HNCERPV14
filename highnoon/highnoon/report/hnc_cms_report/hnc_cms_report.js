// Copyright (c) 2023, 	kiran.c@indictrans.in and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["HNC CMS Report"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options":"Company",
			"width": 100,
			"reqd":0,
		},
		{
			"fieldname":"from",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": 80,
			// "reqd":0,
			// "default": dateutil.year_start()
		},
		{
			"fieldname":"to",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": 80,
			// "reqd":1,
			// "default": dateutil.year_end()
		},

	]
};
