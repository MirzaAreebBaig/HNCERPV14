frappe.ui.form.on("Job Applicant", {
	refresh: function(frm) {
        if (frappe.user_roles.includes('ZHD-TAT') || frappe.user_roles.includes('Candidate')) {
            frm.clear_custom_buttons(frm);
        }
        if (has_common(frappe.user_roles, ["Hide Attach"]) && frappe.session.user != 'Administrator')
	    {
	    $('.form-attachments').hide();
	    }
        if (has_common(frappe.user_roles, ["Candidate"]) && frappe.session.user != 'Administrator')
	    {
	    $('.form-attachments').hide();
	    }
    }
});
frappe.ui.form.on("Job Applicant", "address", function(frm, cdt, cdn) {
    if(frm.doc.address){
     return frm.call({
      method: "frappe.contacts.doctype.address.address.get_address_display",
      args: {
        "address_dict": frm.doc.address
      },
      callback: function(r) {
       if(r.message)
           frm.set_value("full_address", r.message);
        
      }
        });
    }
    else{
        frm.set_value("full_address", "");
    }
});
//------------