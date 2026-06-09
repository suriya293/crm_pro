# Copyright (c) 2026, Administrator and contributors
# For license information, please see license.txt

import unittest
import frappe
from crm_pro.crm_pro.api import create_lead, update_lead, delete_lead, get_dashboard_metrics
from crm_pro.crm_pro.ai import get_lead_score, predict_deal_success

class TestCRMPro(unittest.TestCase):
    def setUp(self):
        # Clear database test items
        frappe.db.delete("CRM Lead")
        frappe.db.delete("CRM Deal")
        frappe.db.delete("CRM Audit Log")
        frappe.db.commit()

    def test_create_lead_validation(self):
        # Name validation (too short)
        with self.assertRaises(frappe.ValidationError):
            create_lead(lead_name="Jo")

        # Success case
        lead_id = create_lead(lead_name="John Doe", email="john@example.com", mobile="9876543210")
        self.assertTrue(lead_id)
        
        # Verify db insert
        lead_doc = frappe.get_doc("CRM Lead", lead_id)
        self.assertEqual(lead_doc.lead_name, "John Doe")
        self.assertEqual(lead_doc.email, "john@example.com")
        self.assertEqual(lead_doc.mobile, "9876543210")

    def test_duplicate_mobile_validation(self):
        # Create first lead
        create_lead(lead_name="John Doe", email="john@example.com", mobile="9876543210")
        
        # Expect ValidationError on duplicate mobile
        with self.assertRaises(frappe.ValidationError):
            create_lead(lead_name="Jane Doe", email="jane@example.com", mobile="9876543210")

    def test_duplicate_email_validation(self):
        # Create first lead
        create_lead(lead_name="John Doe", email="john@example.com", mobile="9876543210")
        
        # Expect ValidationError on duplicate email
        with self.assertRaises(frappe.ValidationError):
            create_lead(lead_name="Jane Doe", email="john@example.com", mobile="1122334455")

    def test_lead_deletion_audit_log(self):
        lead_id = create_lead(lead_name="Dave Smith", email="dave@example.com")
        delete_lead(lead_id)
        
        # Check audit log insertion
        logs = frappe.get_all("CRM Audit Log", filters={"ref_name": lead_id, "action": "Delete"})
        self.assertEqual(len(logs), 1)

    def test_dashboard_metrics(self):
        # Create lead and deal
        lead_id = create_lead(lead_name="Client A", stage="LEAD")
        
        deal = frappe.new_doc("CRM Deal")
        deal.deal_name = "Deal for Client A"
        deal.lead = lead_id
        deal.deal_value = 5000.0
        deal.deal_status = "Won"
        deal.insert()
        
        metrics = get_dashboard_metrics()
        self.assertEqual(metrics.get("total_leads"), 1)
        self.assertEqual(metrics.get("total_revenue"), 5000.0)

    def test_ai_lead_scoring(self):
        lead_id = create_lead(
            lead_name="High Intent Client", 
            email="intent@example.com", 
            mobile="9988776655", 
            company_name="Enterprise Co", 
            source="Referral"
        )
        
        score_res = get_lead_score(lead_id)
        # 30 base + 10 email + 10 mobile + 10 company + 25 referral source = 85
        self.assertEqual(score_res.get("score"), 85)

    def test_ai_deal_success_prediction(self):
        deal = frappe.new_doc("CRM Deal")
        deal.deal_name = "Enterprise Deal"
        deal.deal_value = 12000.0
        deal.deal_stage = "Proposal Sent"
        deal.forecast_category = "Commit"
        deal.insert()
        
        pred = predict_deal_success(deal.name)
        # base 0.4 + Proposal Sent boost 0.2 + Commit boost 0.3 = 0.9
        self.assertEqual(pred.get("success_probability"), 0.9)

    def test_whatsapp_outbound(self):
        # Setup settings
        settings = frappe.get_doc("CRM Settings")
        settings.enable_whatsapp_integration = 1
        settings.whatsapp_access_token = "mock_token"
        settings.whatsapp_phone_number_id = "12345"
        settings.save(ignore_permissions=True)
        
        lead_id = create_lead(lead_name="WhatsApp Client", mobile="+919876543210")
        
        from crm_pro.crm_pro.meta import send_whatsapp_message
        res = send_whatsapp_message(lead_id, "Hello from CRM Pro!")
        self.assertTrue(res.get("messages"))
        
        # Verify logs
        logs = frappe.get_all("CRM WhatsApp Log", filters={"lead": lead_id, "direction": "Outbound"})
        self.assertEqual(len(logs), 1)

    def test_facebook_leadgen_job(self):
        # Trigger background processing
        from crm_pro.crm_pro.jobs import fetch_and_create_facebook_lead
        fetch_and_create_facebook_lead("lead_999")
        
        # Verify creation
        lead = frappe.db.get_value("CRM Lead", {"source": "Facebook Ads"}, ["name", "lead_name"], as_dict=True)
        self.assertTrue(lead)
        self.assertEqual(lead.lead_name, "Facebook Lead lead_999")

