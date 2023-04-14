frappe.ui.form.on('Item', {
	onload: function(frm) {
		frm.set_query('employee', () => {
			return {
				filters: {
					status: 'Active'
				}
			}
		})
		frm.doc.customer_items.forEach(i=>{
			i.ref_code = frm.doc.wo_po_id
			i.work_order_date = frm.doc.work_order_date
		})

	},
	employee(frm)    {
	    if(frm.doc.employee) {
			frappe.db.get_value('Employee', frm.doc.employee, 'status')
			.then(r => {
				if (r.message.status != 'Active') {
					frm.set_value("employee", null);
					frm.set_value("full_name", null);
				}
			})
	        frm.set_value("standard_rate", frm.doc.billing);
		    frm.refresh_field("standard_rate");
	    }
	},
	emp_customer(frm)   {
	    $.each(frm.doc.customer_items || [], function(i, v) {
			frappe.model.set_value(v.doctype, v.name, "customer_name", frm.doc.emp_customer);
            frappe.model.set_value(v.doctype, v.name, "ref_code", frm.doc.work_order_no);
			frappe.model.set_value(v.doctype, v.name, "work_order_date", frm.doc.work_order_date);
			frm.refresh_field("customer_items");
		})
        
    },
    item_cost_center(frm)   {
	    $.each(frm.doc.item_defaults || [], function(i, v) {
			frappe.model.set_value(v.doctype, v.name, "selling_cost_center", frm.doc.item_cost_center);
            frm.refresh_field("item_defaults");
		})
        
    }
})
    
  //----------  