frappe.ui.form.on('Timesheet', {
    refresh: function(frm) {
        // Add a custom button to create attendance records
        frm.add_custom_button(__('Create Attendance Records'), function() {
            frappe.call({
                method: "highnoon.highnoon.custom_script.timesheet.timesheet.create_attendance_from_timesheets",
                args: {
                    timesheet_name: frm.doc.name
                },
                callback: function(response) {
                    if (response.message) {
                        frappe.msgprint(__("Attendance records created successfully"));
                    }
                },
                error: function(error) {
                    frappe.msgprint(__("There was an error creating the attendance records"));
                }
            });
        });
    },
    time_logs_add: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        row.activity_type = 'Attendance';
        frm.refresh_field('time_logs');
    }
});
