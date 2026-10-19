frappe.ui.form.on('Job Offer', {
    before_save(frm){
        frm.doc.annual_gross_salary = frm.doc.base * 12;
        refresh_field("annual_gross_salary");
        frm.doc.monthly_basic_amount = frm.doc.base * 0.5;
        refresh_field("monthly_basic_amount");
        frm.doc.annualized_basic= frm.doc.monthly_basic_amount * 12;
        refresh_field("annualized_basic");
        frm.doc.monthly_hra= frm.doc.monthly_basic_amount * 0.4;
        refresh_field("monthly_hra");
        frm.doc.annualized_hra_amount= frm.doc.monthly_hra * 12;
        refresh_field("annualized_hra_amount");
        frm.doc.monthly_transport_allowance_amount= 1600;
        refresh_field("monthly_transport_allowance_amount");
        frm.doc.annualized_transport_allowance_amount= frm.doc.monthly_transport_allowance_amount * 12;
        refresh_field("annualized_transport_allowance_amount");
        frm.doc.monthly_bonus_amount = frm.doc.base * 0.0833;
        refresh_field("monthly_bonus_amount");
        frm.doc.annualized__bonus_amount= frm.doc.monthly_bonus_amount * 12;
        refresh_field("annualized__bonus_amount");
        frm.doc.monthly_special_allowance_amount = frm.doc.base - frm.doc.monthly_basic_amount - frm.doc.monthly_hra -frm.doc.monthly_transport_allowance_amount - frm.doc.monthly_bonus_amount;
        refresh_field("monthly_special_allowance_amount");
        frm.doc.annualized_special_allowance_amount= frm.doc.monthly_special_allowance_amount * 12;
        refresh_field("annualized_special_allowance_amount");
        /*//////////////////////////////////////// ESIC Employer  calculation/////////////////////*/    
        if(frm.doc.esic_required == "Yes"){
        if (frm.doc.base <= 15000){
        frm.doc.monthly_esic_employer_contribution_amount = frm.doc.base * 1.75/100;
        refresh_field("monthly_esic_employer_contribution_amount");
        frm.doc.annualized_esic_employer_contribution_amount = frm.doc.monthly_esic_employer_contribution_amount * 12;
        refresh_field("annualized_esic_employer_contribution_amount");
        }
        if (frm.doc.base > 15000){
        frm.doc.monthly_esic_employer_contribution_amount = 0;
        refresh_field("monthly_esic_employer_contribution_amount");
        frm.doc.annualized_esic_employer_contribution_amount = 0;
        refresh_field("annualized_esic_employer_contribution_amount");
        }

        }
        if(frm.doc.esic_required == "No"){
        frm.doc.monthly_esic_employer_contribution_amount = 0;
        refresh_field("monthly_esic_employer_contribution_amount");
        frm.doc.annualized_esic_employer_contribution_amount = 0;
        refresh_field("annualized_esic_employer_contribution_amount");

        }
        /*//////////////////////////////////////// ESIC Employee  calculation/////////////////////*/    
        if(frm.doc.esic_required == "Yes"){
        if (frm.doc.base <= 15000){
            frm.doc.monthly_esic_employee_contribution = frm.doc.base * 1.75/100;
            refresh_field("monthly_esic_employee_contribution");
            frm.doc.annualized_esic_employee_contribution = frm.doc.monthly_esic_employee_contribution * 12;
            refresh_field("annualized_esic_employee_contribution");
            }
            if (frm.doc.base > 15000){
            frm.doc.monthly_esic_employee_contribution = 0;
            refresh_field("monthly_esic_employee_contribution");
            frm.doc.annualized_esic_employee_contribution = 0;
            refresh_field("annualized_esic_employee_contribution");
            }
        } 
        if(frm.doc.esic_required == "No"){
            frm.doc.monthly_esic_employee_contribution = 0;
            refresh_field("monthly_esic_employee_contribution");
            frm.doc.annualized_esic_employee_contribution = 0;
            refresh_field("annualized_esic_employee_contribution");
    
            }
       
               /*---/*-------------------------------------pf_employee_contribution_amount----------------------- */
        if (frm.doc.pf_required == "Yes") {
            // Check if custom_pf_type is "Standard"
            if (frm.doc.custom_pf_type == "Standard") {
                // PF = IF(Basic > 25000, 3000, Basic * 12%)
                if (frm.doc.monthly_basic_amount <= 25000) {
                    frm.doc.monthly_pf_employee_contribution_amount = frm.doc.monthly_basic_amount * 12 / 100;
                    refresh_field("monthly_pf_employee_contribution_amount");
                    frm.doc.annualized_pf_employee_contribution_amount = frm.doc.monthly_pf_employee_contribution_amount * 12;
                    refresh_field("annualized_pf_employee_contribution_amount");
                }
                if (frm.doc.monthly_basic_amount > 25000) {
                    frm.doc.monthly_pf_employee_contribution_amount = 3000;
                    refresh_field("monthly_pf_employee_contribution_amount");
                    frm.doc.annualized_pf_employee_contribution_amount = frm.doc.monthly_pf_employee_contribution_amount * 12;
                    refresh_field("annualized_pf_employee_contribution_amount");
                }
            }
            // Check if custom_pf_type is "VPF"
            else if (frm.doc.custom_pf_type == "VPF") {
                frm.doc.monthly_pf_employee_contribution_amount = frm.doc.monthly_basic_amount * 12 / 100;
                refresh_field("monthly_pf_employee_contribution_amount");
                frm.doc.annualized_pf_employee_contribution_amount = frm.doc.monthly_pf_employee_contribution_amount * 12;
                refresh_field("annualized_pf_employee_contribution_amount");
            }
        }
        if (frm.doc.pf_required == "No") {
            frm.doc.monthly_pf_employee_contribution_amount = 0;
            refresh_field("monthly_pf_employee_contribution_amount");
            frm.doc.annualized_pf_employee_contribution_amount = frm.doc.monthly_pf_employee_contribution_amount * 12;
            refresh_field("annualized_pf_employee_contribution_amount");
        }

        /*----------------------------------------pf_employer_contribution_amount----------------------- */
        if (frm.doc.pf_required == "Yes") {
            // Apply the same logic for employer contribution when pf_required is "Yes"
            if (frm.doc.custom_pf_type == "Standard") {
                // PF = IF(Basic > 25000, 3000, Basic * 12%)
                if (frm.doc.monthly_basic_amount <= 25000) {
                    frm.doc.monthly_pf_employer_contribution_amount = frm.doc.monthly_basic_amount * 12 / 100;
                    refresh_field("monthly_pf_employer_contribution_amount");
                    frm.doc.annualized_pf_employer_contribution = frm.doc.monthly_pf_employer_contribution_amount * 12;
                    refresh_field("annualized_pf_employer_contribution");
                }
                if (frm.doc.monthly_basic_amount > 25000) {
                    frm.doc.monthly_pf_employer_contribution_amount = 3000;
                    refresh_field("monthly_pf_employer_contribution_amount");
                    frm.doc.annualized_pf_employer_contribution = frm.doc.monthly_pf_employer_contribution_amount * 12;
                    refresh_field("annualized_pf_employer_contribution");
                }
            }
            // If custom_pf_type is "VPF", the employer contribution stays as per "Standard"
            else if (frm.doc.custom_pf_type == "VPF") {
                frm.doc.monthly_pf_employer_contribution_amount = frm.doc.monthly_basic_amount * 12 / 100;
                refresh_field("monthly_pf_employer_contribution_amount");
                frm.doc.annualized_pf_employer_contribution = frm.doc.monthly_pf_employer_contribution_amount * 12;
                refresh_field("annualized_pf_employer_contribution");
            }
        }
        if (frm.doc.pf_required == "No") {
            frm.doc.monthly_pf_employer_contribution_amount = 0;
            refresh_field("monthly_pf_employer_contribution_amount");
            frm.doc.annualized_pf_employer_contribution = frm.doc.monthly_pf_employer_contribution_amount * 12;
            refresh_field("annualized_pf_employer_contribution");
        }

            frm.doc.monthly_professional_tax_amount = 200;
            refresh_field("monthly_professional_tax_amount");
            frm.doc.annualized_professional_tax_amount = frm.doc.monthly_professional_tax_amount * 12;
            refresh_field("annualized_professional_tax_amount");
           
            frm.doc.total_income = frm.doc.annual_gross_salary - 50000 -frm.doc.annualized_pf_employee_contribution_amount - frm.doc.annualized_professional_tax_amount;
            refresh_field("total_income");
            /* -----------------------------Income Tax Calculation ------------------ */ 
            /*------------------------------ from 250001 to 500000p---------------*/
            frm.doc._income_upto_rs_250000_ = 0;
            refresh_field("_income_upto_rs_250000_");
            
            if(frm.doc.total_income > 250000 && frm.doc.total_income < 500000){
                frm.doc._from_rs_250001_to_rs_500000_ = ((frm.doc.total_income-250000) *0.05);
                refresh_field("_from_rs_250001_to_rs_500000_");
            }
            if(frm.doc.total_income > 500000){
                frm.doc._from_rs_250001_to_rs_500000_ = 12500;
                refresh_field("_from_rs_250001_to_rs_500000_");
            }
            if(frm.doc.total_income < 250000){
                frm.doc._from_rs_250001_to_rs_500000_ = 0;
                refresh_field("_from_rs_250001_to_rs_500000_");
            }
              /*------------------------------ from 500001 to 1000000---------------*/
              
            if(frm.doc.total_income < 500000){
                frm.doc._from_rs_500001_to_rs_1000000_ = 0;
                refresh_field("_from_rs_500001_to_rs_1000000_");
            }
            if(frm.doc.total_income > 1000000){
                frm.doc._from_rs_500001_to_rs_1000000_ = 100000;
                refresh_field("_from_rs_500001_to_rs_1000000_");
            }
            if(frm.doc.total_income > 500000 && frm.doc.total_income < 1000000){
                frm.doc._from_rs_500001_to_rs_1000000_ = ((frm.doc.total_income-500000)*0.2);
                refresh_field("_from_rs_500001_to_rs_1000000_");
            }
            /*------------------------------  Above Rs. 10,00,000 ---------------*/
            
            if(frm.doc.total_income > 1000000){
                frm.doc._above_rs_1000000_ = ((frm.doc.total_income-1000000)*0.3);
                refresh_field("_above_rs_1000000_");
            }
            if(frm.doc.total_income < 1000000){
                frm.doc._above_rs_1000000_ = 0;
                refresh_field("_above_rs_1000000_");
            }
            /*--------------------------------Total tax on taxable incom------*/
            frm.doc._total_tax_on_taxable_income_pa_ =frm.doc._income_upto_rs_250000_ + frm.doc._from_rs_250001_to_rs_500000_ + frm.doc._from_rs_500001_to_rs_1000000_ + frm.doc._above_rs_1000000_ ;
            refresh_field("_total_tax_on_taxable_income_pa_");
            /*------------------Rebate ------------------------------*/
            
            if(frm.doc.total_income > 500000){
                frm.doc.rebate = 0;
                refresh_field("rebate");
            }
            if(frm.doc._total_tax_on_taxable_income_pa_){
                frm.doc.rebate = 0;
                refresh_field("rebate");
            }
            
            if(frm.doc._total_tax_on_taxable_income_pa_ <= 12500){
                frm.doc.rebate = frm.doc._total_tax_on_taxable_income_pa_;
                refresh_field("rebate");
            }
            /*---------------------------------------Balance Tax-------------------------*/
            frm.doc.balance_tax =frm.doc._total_tax_on_taxable_income_pa_ - frm.doc.rebate;
            refresh_field("balance_tax");
            /*---------------------------------- Health & Education Cess @ 4% --------------------*/
            frm.doc.health_and_education_cess =(frm.doc.balance_tax * 0.04);
            refresh_field("health_and_education_cess");
            /*-------------------------------  Total Tax Liability ---------------------*/
            frm.doc.total_tax_liability=frm.doc.balance_tax + frm.doc.health_and_education_cess;
            refresh_field("total_tax_liability");

            /* -----------------------------Income Tax Calculation (New Regime) ------------------ */
            frm.doc.custom_standard_deduction_new_regime = 75000;
            refresh_field("custom_standard_deduction_new_regime");
            frm.doc.custom_total_income_new_regime = Math.max(frm.doc.annual_gross_salary - frm.doc.custom_standard_deduction_new_regime, 0);
            refresh_field("custom_total_income_new_regime");

            let new_regime_income = frm.doc.custom_total_income_new_regime;
            let new_regime_slabs = [
                ["custom_income_upto_rs_400000_new_regime", 0, 400000, 0],
                ["custom_from_rs_400001_to_rs_800000_new_regime", 400000, 800000, 0.05],
                ["custom_from_rs_800001_to_rs_1200000_new_regime", 800000, 1200000, 0.10],
                ["custom_from_rs_1200001_to_rs_1600000_new_regime", 1200000, 1600000, 0.15],
                ["custom_from_rs_1600001_to_rs_2000000_new_regime", 1600000, 2000000, 0.20],
                ["custom_from_rs_2000001_to_rs_2400000_new_regime", 2000000, 2400000, 0.25],
                ["custom_above_rs_2400000_new_regime", 2400000, Infinity, 0.30],
            ];
            frm.doc.custom__total_tax_on_taxable_income_pa_new_regime = 0;
            new_regime_slabs.forEach(([fieldname, from, to, rate]) => {
                frm.doc[fieldname] = Math.max(Math.min(new_regime_income, to) - from, 0) * rate;
                refresh_field(fieldname);
                frm.doc.custom__total_tax_on_taxable_income_pa_new_regime += frm.doc[fieldname];
            });
            refresh_field("custom__total_tax_on_taxable_income_pa_new_regime");
            /*------------------Rebate u/s 87A (max 60,000 if income <= 12 lakhs, with marginal relief above) ------------------------------*/
            let new_regime_tax = frm.doc.custom__total_tax_on_taxable_income_pa_new_regime;
            if (new_regime_income <= 1200000) {
                frm.doc.custom_rebate_new_regime = Math.min(new_regime_tax, 60000);
            } else {
                frm.doc.custom_rebate_new_regime = Math.max(new_regime_tax - (new_regime_income - 1200000), 0);
            }
            refresh_field("custom_rebate_new_regime");
            /*---------------------------------------Balance Tax-------------------------*/
            frm.doc.custom_balance_tax_new_regime = new_regime_tax - frm.doc.custom_rebate_new_regime;
            refresh_field("custom_balance_tax_new_regime");
            /*---------------------------------- Health & Education Cess @ 4% --------------------*/
            frm.doc.custom_health_and_education_cess_new_regime = frm.doc.custom_balance_tax_new_regime * 0.04;
            refresh_field("custom_health_and_education_cess_new_regime");
            /*-------------------------------  Total Tax Liability ---------------------*/
            frm.doc.custom_total_tax_liability_new_regime = frm.doc.custom_balance_tax_new_regime + frm.doc.custom_health_and_education_cess_new_regime;
            refresh_field("custom_total_tax_liability_new_regime");




        

           

        },
        
    onload: function(frm){
        frm.set_query("company_address_name", function() {
            return {
                    "filters": {
                    "address_title": frm.doc.company
                }
            };
        });
    },
    refresh: function(frm) {
        if (has_common(frappe.user_roles, ["Candidate"]) && frappe.session.user != 'Administrator')
	    {
	    $('.form-attachments').hide();
	    }
    }
})