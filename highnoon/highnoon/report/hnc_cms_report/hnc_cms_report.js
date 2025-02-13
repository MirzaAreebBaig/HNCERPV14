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
			"fieldname":"start_date",
			"label": __("Start Date"),
			"fieldtype": "Date",
			"width": 80,
			// "reqd":0,
			// "default": dateutil.year_start()
		},
		{
			"fieldname":"end_date",
			"label": __("End Date"),
			"fieldtype": "Date",
			"width": 80,
			// "reqd":1,
			// "default": dateutil.year_end()
		},

	]
};