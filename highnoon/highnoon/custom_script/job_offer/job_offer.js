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
        frm.doc.monthly_pf_employer_contribution_amount= 1800;
        refresh_field("monthly_pf_employer_contribution_amount")
        frm.doc.annualized_pf_employer_contribution= frm.doc.monthly_pf_employer_contribution_amount * 12;
        refresh_field("annualized_pf_employer_contribution");
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
                if (frm.doc.monthly_basic_amount <= 15000) {
                    frm.doc.monthly_pf_employee_contribution_amount = frm.doc.monthly_basic_amount * 12 / 100;
                    refresh_field("monthly_pf_employee_contribution_amount");
                    frm.doc.annualized_pf_employee_contribution_amount = frm.doc.monthly_pf_employee_contribution_amount * 12;
                    refresh_field("annualized_pf_employee_contribution_amount");
                }
                if (frm.doc.monthly_basic_amount > 15000) {
                    frm.doc.monthly_pf_employee_contribution_amount = 1800;
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
                if (frm.doc.monthly_basic_amount <= 15000) {
                    frm.doc.monthly_pf_employer_contribution_amount = frm.doc.monthly_basic_amount * 12 / 100;
                    refresh_field("monthly_pf_employer_contribution_amount");
                    frm.doc.annualized_pf_employer_contribution = frm.doc.monthly_pf_employer_contribution_amount * 12;
                    refresh_field("annualized_pf_employer_contribution");
                }
                if (frm.doc.monthly_basic_amount > 15000) {
                    frm.doc.monthly_pf_employer_contribution_amount = 1800;
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
            frm.doc.annualized_pf_employer_contribution = frm.doc.monthly_pf_employee_contribution_amount * 12;
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