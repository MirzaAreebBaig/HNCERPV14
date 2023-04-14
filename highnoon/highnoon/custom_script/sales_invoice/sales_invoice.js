frappe.ui.form.on('Sales Invoice', {
    before_save(frm){
            frm.doc.total_amount = (frm.doc.total - (0.1 * frm.doc.total) + (0.18 * frm.doc.total));
            refresh_field("total_amount ");
            if(frm.doc.item) {
                frappe.db.get_value("Item", {"name":frm.doc.item }, ["address"], (r)=>{
                        frm.doc.customer_address = r.address
                })
        }
        },
    onload: function(frm){
        frm.set_query("customer_address", function() {
            return {
                   "filters": {
                    "address_title": frm.doc.customer
                }
            };
        });
        },
    item(frm)    {
        if(frm.doc.item) {
        frappe.db.get_value("Item", {"name":frm.doc.item }, ["emp_customer", "item_cost_center", "address", "wo_po_id", "work_order_date" ], (r)=>{

            frm.set_value("customer", r.emp_customer);
            frm.set_value("cost_center", r.item_cost_center);
            frm.set_value("po_no", r.wo_po_id);
            frm.set_value("po_date", r.work_order_date);
            
        })
        }
        },
    
   item(frm){
        
        $.each(frm.doc.items || [], function(i, v) {
                frappe.model.set_value(v.doctype, v.name, "item_code", frm.doc.item);
                frm.refresh_field("items");
        })
        },
    end_date1(frm){
        if (frm.doc.end_date1){
        frappe.db.get_value("Item Price", {"item_code":frm.doc.item, "valid_from":["<=",frm.doc.start_date1], "valid_upto":[">=", frm.doc.end_date1] }, ["valid_from", "valid_upto", "price_list_rate"], (r)=>{

        $.each(frm.doc.items || [], function(i, v) {
                    frappe.model.set_value(v.doctype, v.name, "rate", r.price_list_rate);
                    frm.refresh_field("items");
            })
        })
      }    
    }
})
