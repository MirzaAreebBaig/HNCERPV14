import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

OLD_SLAB_FIELDS = [
    "custom__income_upto_rs_300000_new_regime",
    "custom__from_rs_300001_to_rs_600000new_regime_",
    "custom__from_rs_600001_to_rs_900000new_regime_",
    "custom__from_rs_900001_to_rs_1200000new_regime_",
    "custom__from_rs_1200001_to_rs_1500000_new_regime_",
    "custom_above_1500000_new_regime",
]

NEW_SLAB_FIELDS = [
    ("custom_income_upto_rs_400000_new_regime", "Income upto Rs 400000 (New Regime)"),
    ("custom_from_rs_400001_to_rs_800000_new_regime", "From Rs 400001 to Rs 800000 @5% (New Regime)"),
    ("custom_from_rs_800001_to_rs_1200000_new_regime", "From Rs 800001 to Rs 1200000 @10% (New Regime)"),
    ("custom_from_rs_1200001_to_rs_1600000_new_regime", "From Rs 1200001 to Rs 1600000 @15% (New Regime)"),
    ("custom_from_rs_1600001_to_rs_2000000_new_regime", "From Rs 1600001 to Rs 2000000 @20% (New Regime)"),
    ("custom_from_rs_2000001_to_rs_2400000_new_regime", "From Rs 2000001 to Rs 2400000 @25% (New Regime)"),
    ("custom_above_rs_2400000_new_regime", "Above Rs 2400000 @30% (New Regime)"),
]

# Start of the refresh-time new regime calculation in the "job offer" Client Script,
# now handled in before_save of highnoon/custom_script/job_offer/job_offer.js
CLIENT_SCRIPT_NEW_REGIME_MARKER = "frm.doc.custom_total_income_new_regime = frm.doc.annual_gross_salary - 50000;"


def execute():
    fields = [
        {
            "fieldname": "custom_standard_deduction_new_regime",
            "label": "Standard Deduction (New Regime)",
            "fieldtype": "Currency",
            "insert_after": "custom_income_tax_calculationnew_regime",
            "read_only": 1,
        },
        {
            "fieldname": "custom_total_income_new_regime",
            "label": "Total Income (New Regime)",
            "fieldtype": "Currency",
            "insert_after": "custom_standard_deduction_new_regime",
        },
    ]
    insert_after = "custom_above_1500000_new_regime"
    for fieldname, label in NEW_SLAB_FIELDS:
        fields.append({
            "fieldname": fieldname,
            "label": label,
            "fieldtype": "Currency",
            "insert_after": insert_after,
            "read_only": 1,
        })
        insert_after = fieldname
    fields.append({
        "fieldname": "custom__total_tax_on_taxable_income_pa_new_regime",
        "label": " Total Tax on Taxable Income PA (New Regime)",
        "fieldtype": "Currency",
        "insert_after": insert_after,
    })
    fields.append({
        "fieldname": "custom_rebate_new_regime",
        "label": "Rebate u/s 87A (New Regime)",
        "fieldtype": "Currency",
        "insert_after": "custom_column_break_ei8q9",
    })
    create_custom_fields({"Job Offer": fields}, update=True)

    # Keep old slab fields for submitted offers, but hide them
    for fieldname in OLD_SLAB_FIELDS:
        name = frappe.db.get_value("Custom Field", {"dt": "Job Offer", "fieldname": fieldname})
        if name:
            frappe.db.set_value("Custom Field", name, "hidden", 1)

    remove_new_regime_from_client_script()
    frappe.clear_cache(doctype="Job Offer")


def remove_new_regime_from_client_script():
    if not frappe.db.exists("Client Script", "job offer"):
        return
    script = frappe.db.get_value("Client Script", "job offer", "script") or ""
    marker = script.find(CLIENT_SCRIPT_NEW_REGIME_MARKER)
    if marker == -1:
        return
    # Cut from the "frappe.ui.form.on(" that opens the block containing the marker
    block_start = script.rfind("frappe.ui.form.on(", 0, marker)
    if block_start == -1:
        return
    frappe.db.set_value("Client Script", "job offer", "script", script[:block_start].rstrip() + "\n")
