frappe.ui.form.on('Payment Entry', {
    get_amount: function(frm) {
      frm.doc.references.forEach(i=>{
            frappe.db.get_value("Sales Invoice", {"name": i.reference_name}, ["total_amount","cost_center"], (r)=>{
              i.amount = r.total_amount
              i.cost_center = r.cost_center
              frm.refresh_fields("references");
              
          })
	     })
      }
    })
 
 
