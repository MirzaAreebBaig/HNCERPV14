frappe.ui.form.on('Payment Entry', {
    get_amount: function(frm) {
      frm.doc.references.forEach(i=>{
            frappe.db.get_value("Sales Invoice", {"name": i.reference_name}, "total_amount", (r)=>{
              i.amount = r.total_amount
              frm.refresh_fields("references");
          })
	     })
	     

	}
})
