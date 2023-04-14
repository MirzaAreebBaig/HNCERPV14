frappe.ui.form.on('Item Price', {
    
	item_code(frm){
	    if(frm.doc.item_code) {
            frappe.db.get_value("Item", {"name":frm.doc.item_code }, ["standard_rate","start_date","end_date"], (r)=>{
			frm.set_value("price_list_rate", r.standard_rate);
            frm.set_value("valid_from", r.start_date);
            frm.set_value("valid_upto", r.end_date);
            })
	    }
    
	},
})