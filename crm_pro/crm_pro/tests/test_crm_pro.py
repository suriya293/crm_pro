import logging
from ratelimit import limits as ratelimit
# Copyright (c) 2026, Administrator and contributors
# For license information, please see license.txt

import unittest
import frappe
from crm_pro.api import create_lead, update_lead, delete_lead, get_dashboard_metrics, create_deal
from crm_pro.ai import get_lead_score, predict_deal_success

class TestCRMPro(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")
        # Clear database test items
        frappe.db.delete("CRM Lead")
        frappe.db.delete("CRM Deal")
        frappe.db.delete("CRM Audit Log")
        
        # Ensure default pipeline, stages, and settings exist in test database
        from crm_pro.install import create_default_pipeline_and_stages, create_default_settings
        create_default_pipeline_and_stages()
        create_default_settings()
        
        frappe.db.commit()


    def test_create_lead_validation(self):
        # Name validation (too short)
        with self.assertRaises(frappe.ValidationError):
            create_lead(lead_name="Jo")

        # Success case
        lead_id = create_lead(lead_name="John Doe", email="john@example.com", mobile="+919876543210")
        self.assertTrue(lead_id)
        
        # Verify db insert
        lead_doc = frappe.get_doc("CRM Lead", lead_id)
        self.assertEqual(lead_doc.lead_name, "John Doe")
        self.assertEqual(lead_doc.email, "john@example.com")
        self.assertEqual(lead_doc.mobile, "+919876543210")

    def test_duplicate_mobile_validation(self):
        # Create first lead
        create_lead(lead_name="John Doe", email="john@example.com", mobile="+919876543210")
        
        # Expect ValidationError on duplicate mobile
        with self.assertRaises(frappe.ValidationError):
            create_lead(lead_name="Jane Doe", email="jane@example.com", mobile="+919876543210")

    def test_duplicate_email_validation(self):
        # Create first lead
        create_lead(lead_name="John Doe", email="john@example.com", mobile="+919876543210")
        
        # Expect ValidationError on duplicate email
        with self.assertRaises(frappe.ValidationError):
            create_lead(lead_name="Jane Doe", email="john@example.com", mobile="+918888800002")

    def test_lead_deletion_audit_log(self):
        lead_id = create_lead(lead_name="Dave Smith", email="dave@example.com", mobile="+919876543212")
        delete_lead(lead_id)
        
        # Check audit log insertion
        logs = frappe.get_all("CRM Audit Log", filters={"ref_name": lead_id, "action": "Delete"})
        self.assertEqual(len(logs), 1)

    def test_dashboard_metrics(self):
        # Create lead and deal
        lead_id = create_lead(lead_name="Client A", stage="LEAD", mobile="+919876543213")
        
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
            mobile="+919988776655", 
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
        deal.deal_stage = "PROPOSAL SENT"
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
        
        from crm_pro.meta import send_whatsapp_message
        res = send_whatsapp_message(lead_id, "Hello from CRM Pro!")
        self.assertTrue(res.get("messages"))
        
        # Verify logs
        logs = frappe.get_all("CRM WhatsApp Log", filters={"lead": lead_id, "direction": "Outbound"})
        self.assertEqual(len(logs), 1)

    def test_facebook_leadgen_job(self):
        # Trigger background processing
        from crm_pro.jobs import fetch_and_create_facebook_lead
        fetch_and_create_facebook_lead("lead_999")
        
        # Verify creation
        lead = frappe.db.get_value("CRM Lead", {"source": "Facebook Ads"}, ["name", "lead_name"], as_dict=True)
        self.assertTrue(lead)
        self.assertEqual(lead.lead_name, "Facebook Lead lead_999")

    def test_unauthorized_endpoints(self):
        # Create a dummy deal as Administrator first
        lead_id = create_lead(lead_name="Client Temp", stage="LEAD", mobile="+919876543214")
        
        deal = frappe.new_doc("CRM Deal")
        deal.deal_name = "Temp Deal"
        deal.lead = lead_id
        deal.deal_value = 1000.0
        deal.deal_status = "Open"
        deal.insert()
        deal_name = deal.name
        
        # Switch session user to Guest
        frappe.set_user("Guest")
        
        try:
            # Calling create_deal should throw PermissionError
            with self.assertRaises(frappe.PermissionError):
                create_deal(deal_name="Guest Deal", lead="some_lead", deal_value=100.0)

            # Calling update_deal_stage should throw PermissionError
            with self.assertRaises(frappe.PermissionError):
                from crm_pro.api import update_deal_stage
                update_deal_stage(name=deal_name, deal_stage="some_stage")

            # Calling get_pipeline should throw PermissionError
            with self.assertRaises(frappe.PermissionError):
                from crm_pro.api import get_pipeline
                get_pipeline()
        finally:
            # Restore session user to Administrator
            frappe.set_user("Administrator")

    def test_webhook_signatures(self):
        from crm_pro.meta import verify_meta_signature
        import hmac
        import hashlib
        
        # Setup settings with facebook app secret
        settings = frappe.get_doc("CRM Settings")
        settings.facebook_app_secret = "secret123"
        settings.save(ignore_permissions=True)
        frappe.clear_cache(doctype="CRM Settings")
        
        class MockRequest:
            def __init__(self, headers, data):
                self.headers = headers
                self.data = data
        
        payload = b'{"object": "page"}'
        
        # 1. Test invalid signature
        req_invalid = MockRequest({"X-Hub-Signature-256": "sha256=invalidhash"}, payload)
        self.assertFalse(verify_meta_signature(req_invalid))
        
        # 2. Test valid signature
        mac = hmac.new(b"secret123", msg=payload, digestmod=hashlib.sha256)
        valid_signature = f"sha256={mac.hexdigest()}"
        req_valid = MockRequest({"X-Hub-Signature-256": valid_signature}, payload)
        self.assertTrue(verify_meta_signature(req_valid))
        
        # Restore settings
        settings.facebook_app_secret = ""
        settings.save(ignore_permissions=True)

    def test_crm_settings_and_notes(self):
        from crm_pro.api import save_crm_settings, get_crm_settings, get_pipeline_stages, create_crm_note, get_crm_notes, delete_crm_note
        
        # 1. Test Settings
        save_crm_settings(company_name="New Test Corp", enable_ai_suggestions=0)
        settings = get_crm_settings()
        self.assertEqual(settings.get("company_name"), "New Test Corp")
        self.assertEqual(settings.get("enable_ai_suggestions"), 0)
        
        # Restore settings
        save_crm_settings(company_name="Precision CRM", enable_ai_suggestions=1)
        
        # 2. Test Stages
        stages = get_pipeline_stages()
        self.assertTrue(len(stages) > 0)
        
        # 3. Test Notes
        lead_id = create_lead(lead_name="Note Client", mobile="+919876543215")
        note_id = create_crm_note(lead_id, "This is a test note content.")
        self.assertTrue(note_id)
        
        notes = get_crm_notes(lead_id)
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0].content, "This is a test note content.")
        
        delete_crm_note(note_id)
        notes_post_delete = get_crm_notes(lead_id)
        self.assertEqual(len(notes_post_delete), 0)

    def test_forgot_password_token_leak_prevention(self):
        # Authenticate and call forgot_password_endpoint
        from crm_pro.api_auth import forgot_password_endpoint
        
        email = "test_leak@example.com"
        if not frappe.db.exists("User", email):
            user = frappe.get_doc({
                "doctype": "User",
                "email": email,
                "first_name": "TestLeak",
                "enabled": 1,
                "send_welcome_email": 0
            })
            user.insert(ignore_permissions=True)
            
        # Simulate non-test environment (temporarily override frappe.flags.in_test and frappe.conf.developer_mode)
        import json
        from werkzeug.test import EnvironBuilder
        from werkzeug.wrappers import Request
        builder = EnvironBuilder(path="/api/forgot-password", method="POST", data={"email": email})
        frappe.local.request = Request(builder.get_environ())
        frappe.form_dict = frappe.local.request.form.copy()
        frappe.form_dict.email = email
        
        orig_in_test = frappe.flags.in_test
        orig_dev_mode = frappe.conf.developer_mode
        try:
            frappe.flags.in_test = False
            frappe.conf.developer_mode = False
            
            resp = forgot_password_endpoint()
            resp_data = json.loads(resp.get_data(as_text=True))
            
            # Reset token must NOT be returned in production payload
            self.assertNotIn("token", resp_data)
            self.assertEqual(resp_data.get("message"), "If the email exists, a reset code has been sent.")
        finally:
            frappe.flags.in_test = orig_in_test
            frappe.conf.developer_mode = orig_dev_mode
            frappe.local.request = None
            frappe.form_dict = frappe._dict()
            frappe.delete_doc("User", email, ignore_permissions=True)

    def test_get_leads_permission_count_safety(self):
        # Create restricted user
        exec_email = "exec_restricted@example.com"
        if not frappe.db.exists("User", exec_email):
            user = frappe.get_doc({
                "doctype": "User",
                "email": exec_email,
                "first_name": "ExecRestricted",
                "enabled": 1,
                "send_welcome_email": 0
            })
            user.append("roles", {"role": "Sales Executive"})
            user.insert(ignore_permissions=True)
            
        # Clear existing leads for clean test state
        frappe.db.delete("CRM Lead")
        frappe.db.delete("CRM Task")
        frappe.db.commit()
        
        # Lead A: Admin owned
        lead_a = frappe.get_doc({
            "doctype": "CRM Lead",
            "lead_name": "Admin Owned Lead",
            "email": "admin_owned@example.com",
            "mobile": "+919999900991",
            "user": "Administrator",
            "stage": "LEAD"
        }).insert(ignore_permissions=True)
        
        # Lead B: Restricted exec owned
        lead_b = frappe.get_doc({
            "doctype": "CRM Lead",
            "lead_name": "Exec Owned Lead",
            "email": "exec_owned@example.com",
            "mobile": "+919999900992",
            "user": exec_email,
            "stage": "LEAD"
        }).insert(ignore_permissions=True)
        
        # Apply user permission
        up = frappe.get_doc({
            "doctype": "User Permission",
            "user": exec_email,
            "allow": "User",
            "for_value": exec_email
        }).insert(ignore_permissions=True)
        frappe.db.commit()
        
        orig_user = frappe.session.user
        try:
            frappe.set_user(exec_email)
            from crm_pro.api import get_leads
            res = get_leads()
            leads_list = res.get("data", {}).get("leads", [])
            total_count = res.get("data", {}).get("total_count", 0)
            
            # The restricted user should only see lead_b (1 lead), and total_count must equal 1 (not 2!)
            self.assertEqual(len(leads_list), 1)
            self.assertEqual(leads_list[0].get("name"), lead_b.name)
            self.assertEqual(total_count, 1)
        finally:
            frappe.set_user(orig_user)
            frappe.delete_doc("User Permission", up.name, ignore_permissions=True)
            frappe.db.delete("CRM Lead")
            frappe.delete_doc("User", exec_email, ignore_permissions=True)
            frappe.db.commit()

    def test_desk_deletion_block_on_linked_activities(self):
        # Create a lead
        lead_id = create_lead(lead_name="Cancel Block Test", email="block_test@example.com", mobile="+919999900993")
        
        # Attach a task
        task = frappe.get_doc({
            "doctype": "CRM Task",
            "lead": lead_id,
            "task_subject": "Test Block Task",
            "status": "Open"
        }).insert(ignore_permissions=True)
        frappe.db.commit()
        
        # Direct deletion (simulating Desk UI) must fail with LinkExistsError
        with self.assertRaises(frappe.LinkExistsError):
            frappe.delete_doc("CRM Lead", lead_id)
            
        # Cleanup task first, then lead should delete successfully
        frappe.delete_doc("CRM Task", task.name, ignore_permissions=True)
        frappe.delete_doc("CRM Lead", lead_id)
        frappe.db.commit()


