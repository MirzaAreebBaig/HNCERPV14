frappe.ui.form.on('Employee', {
    onload: function(frm){
        frm.set_query("customer_address1", function() {
            return {
                query: 'highnoon.highnoon.custom_script.employee.employee.get_customer_addresses',
                filters: {
                    customer: frm.doc.customer
                }
            };
        });
    },
    job_applicants(frm){
        if(frm.doc.job_applicants) {
            frappe.db.get_value('Job Applicant',{"name":frm.doc.job_applicants }, ['applicant_father_name', 'email_id', 'phone_number', 'gender',
            'upper_range', 'client_name', 'deployment_location', 'primay_skill', 'secondary_skill', 'pf', 'pan_card', 'aadhar_card', 'cost_center', 'country', 'currency', 'address', 'job_title', 'designation',  'salutation','date_of_joining','full_address', 'client_name1','client_email_id'], (r)=>{
                
                    frm.set_value('email_id', r.email_id)
                    frm.set_value('father_name', r.applicant_father_name)
                    frm.set_value('primary_skill', r.primay_skill)
                    frm.set_value('secondary_skill', r.secondary_skill)
                    frm.set_value('address', r.address)
                    frm.set_value('currency', r.currency)
                    frm.set_value('cost_center', r.cost_center)
                    frm.set_value('country', r.country)
                    frm.set_value('job_opening', r.job_title)
                    frm.set_value('designation', r.designation)
                    frm.set_value('cell_number', r.phone_number)
                    frm.set_value('provident_fund', r.pf)
                    frm.set_value('ectc', r.upper_range)
                    frm.set_value('customer', r.client_name)
                    frm.set_value('deployment_location', r.deployment_location)
                    frm.set_value('aadhar_number', r.aadhar_card)
                    frm.set_value('pan_number', r.pan_card)
                    frm.set_value('gender', r.gender)
                    frm.set_value('date_of_joining', r.date_of_joining)
                    frm.set_value('permanent_address', r.full_address)
                    frm.set_value('client_entity', r.client_name)
                    frm.set_value('client_name', r.client_name1)
                    frm.set_value('client_email_id', r.client_email_id)



                })
                    frappe.db.get_value('Employee Onboarding', {'job_applicant': frm.doc.job_applicants}, 'wo_po_id', (r)=>{
                    frm.set_value('work_order_number', r.wo_po_id)
                    })
            }
        },
        
    refresh: function(frm) {
        if (has_common(frappe.user_roles, ["Candidate"]) && frappe.session.user != 'Administrator')
	    {
	    $('.form-attachments').hide();
	    }
    }
})
frappe.ui.form.on("Employee", "customer_address1", function(frm, cdt, cdn) {
    if(frm.doc.customer_address1){
     return frm.call({
      method: "frappe.contacts.doctype.address.address.get_address_display",
      args: {
        "address_dict": frm.doc.customer_address1
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
frappe.ui.form.on("Employee", "address", function(frm, cdt, cdn) {
    if(frm.doc.address){
     return frm.call({
      method: "frappe.contacts.doctype.address.address.get_address_display",
      args: {
        "address_dict": frm.doc.address
      },
      callback: function(r) {
       if(r.message)
           frm.set_value("permanent_address", r.message);
        
      }
        });
    }
    else{
        frm.set_value("permanent_address", "");
    }
});
