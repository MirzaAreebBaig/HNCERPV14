// JavaScript Report Script
frappe.query_reports["Pre-Onboarding"] = {
    filters: [
        {
            fieldname: "start_date",
            label: __("Start Date"),
            fieldtype: "Date", // Default to today's date
            reqd: 0 // Make this field mandatory
        },
        {
            fieldname: "end_date",
            label: __("End Date"),
            fieldtype: "Date", // Default to today's date
            reqd: 0 // Make this field mandatory
        }
    ],
    onload: function(report) {
        report.page.add_inner_button(__("Refresh"), function() {
            frappe.query_report.refresh();
        });
    },

    formatter: function(value, row, column, data, default_formatter) {
        // Apply default formatting to get the standard display
        value = default_formatter(value, row, column, data);

        if (!data) {
            return value;
        }

        // Default color for candidate_name and date_of_joining
        const all_fields_yes = data.resigned === 1 &&
                               data.resignation_accepted === 1 &&
                               data.bgv_ir_cleared === 1 &&
                               data.relocated__at_work_location &&
                               data.last_working_date;

        // Conditional styling for applicant_name and joining_date
        if (column.fieldname === "applicant_name" || column.fieldname === "joining_date") {
            if (all_fields_yes) {
                value = `<div style="background-color: #00c928; padding: 2px; border-radius: 2px; color: #F9FAFA;">${value}</div>`; // Green
            } else {
                value = `<div style="background-color: #e21616; padding: 2px; border-radius: 2px; color:white;">${value}</div>`; // Red
            }
        }

        // Conditional styling for resigned, resignation_accepted, relocated_at_work_location, and last_working_date fields
        // Conditional styling for resigned, resignation_accepted, relocated_at_work_location, and last_working_date fields
        if (["resigned", "resignation_accepted", "relocated__at_work_location", "last_working_date", "bgv_ir_cleared"].includes(column.fieldname)) {
            if (column.fieldname === "relocated__at_work_location" && data.relocated__at_work_location) {
                value = `<div style="background-color: #00c928; padding: 2px; border-radius: 2px; color: #F9FAFA">${value}</div>`; // Green
            } else if (column.fieldname === "last_working_date" && data.last_working_date) {
                value = `<div style="background-color: #00c928; padding: 2px; border-radius: 2px; color: #F9FAFA">${value}</div>`; // Green
            } else if (column.fieldname === "bgv_ir_cleared" && data.bgv_ir_cleared === 1) {
                value = `<div style="background-color: #00c928; padding: 2px; border-radius: 2px; color: #F9FAFA">${value}</div>`; // Green
            } else if (data[column.fieldname] === 1) {
                value = `<div style="background-color: #00c928; padding: 2px; border-radius: 2px; color: #F9FAFA">${value}</div>`; // Green
            } else {
                value = `<div style="background-color: #e21616; padding: 2px; border-radius: 2px; color:white;">${value}</div>`; // Red
            }
        }


        return value;
    }
};