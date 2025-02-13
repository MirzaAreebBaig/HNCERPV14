
frappe.query_reports["Attendance Sheet"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.month_start()
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.month_end()
        },
        {
            "fieldname": "employee",
            "label": __("Employee"),
            "fieldtype": "Link",
            "options": "Employee"
        }
    ],
    onload: function(report) {
        report.page.add_inner_button(__('Create Timesheets'), function() {
            let filters = report.get_values();
            
            if (!filters.from_date || !filters.to_date) {
                frappe.msgprint(__("Please set both From Date and To Date"));
                return;
            }
            
            frappe.call({
                method: "highnoon.highnoon.report.attendance_sheet.attendance_sheet.create_timesheets",
                args: {
                    from_date: filters.from_date,
                    to_date: filters.to_date,
                    employee: filters.employee
                },
                callback: function(response) {
                    if (response.message) {
                        frappe.msgprint(__("Timesheets created successfully"));
                    }
                },
                error: function(error) {
                    frappe.msgprint(__("There was an error creating the timesheets"));
                }
            });
        });
    }
};
