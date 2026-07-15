import unittest
import frappe
import json
from crm_pro.api_auth import (
    register_endpoint,
    login_endpoint,
    logout_endpoint,
    change_password_endpoint,
    forgot_password_endpoint,
    reset_password_endpoint,
    profile_endpoint,
    update_mobile_endpoint,
    update_email_endpoint,
    reset_failed_login,
    is_account_locked
)

class DummyRequest:
    def __init__(self):
        self.path = "/api/profile"
        self.method = "GET"
        self.host = "localhost"
        self.scheme = "http"
        self.remote_addr = "127.0.0.1"
        self.headers = {}
        self.environ = {}
        self.data = b""
        self.cookies = {}

class TestCRMProAuth(unittest.TestCase):
    def setUp(self):
        # Print module_app keys for debugging
        print("\nDEBUG module_app keys:", list(frappe.local.module_app.keys()) if getattr(frappe.local, "module_app", None) else "None")
        
        # Mock the request object in local context to avoid unbound Werkzeug proxy errors
        frappe.local.request = DummyRequest()
        
        # Clean up test users
        test_users = ["test_auth_1@example.com", "test_auth_2@example.com", "test_auth_3@example.com", "test_valid_num@example.com", "test_invalid_num@example.com", "user_a@example.com", "user_b@example.com"]
        for email in test_users:
            frappe.db.delete("CRM Audit Log", {"ref_name": email})
            frappe.db.delete("CRM Audit Log", {"user": email})
            profile_name = frappe.db.get_value("CRM User Profile", {"user": email}, "name")
            if profile_name:
                frappe.delete_doc("CRM User Profile", profile_name, ignore_permissions=True)
            if frappe.db.exists("User", email):
                frappe.delete_doc("User", email, ignore_permissions=True)
            reset_failed_login(email)
            
        test_mobiles = ["+919876543210", "+918907654312", "+919999900088", "+919999900001", "+919999900002", "+919999900003", "+919999900009"]
        for mobile in test_mobiles:
            frappe.db.delete("CRM User Profile", {"phone_number": mobile})
            users = frappe.get_all("User", filters={"mobile_no": mobile}, pluck="name")
            for u in users:
                if u != "Administrator":
                    frappe.delete_doc("User", u, ignore_permissions=True)
            
        frappe.db.commit()
        frappe.set_user("Administrator")

    def tearDown(self):
        # Clean up after test
        test_users = ["test_auth_1@example.com", "test_auth_2@example.com", "test_auth_3@example.com", "test_valid_num@example.com", "test_invalid_num@example.com", "user_a@example.com", "user_b@example.com"]
        for email in test_users:
            frappe.db.delete("CRM Audit Log", {"ref_name": email})
            frappe.db.delete("CRM Audit Log", {"user": email})
            profile_name = frappe.db.get_value("CRM User Profile", {"user": email}, "name")
            if profile_name:
                frappe.delete_doc("CRM User Profile", profile_name, ignore_permissions=True)
            if frappe.db.exists("User", email):
                frappe.delete_doc("User", email, ignore_permissions=True)
            reset_failed_login(email)
            
        test_mobiles = ["+919876543210", "+918907654312", "+919999900088", "+919999900001", "+919999900002", "+919999900003", "+919999900009"]
        for mobile in test_mobiles:
            frappe.db.delete("CRM User Profile", {"phone_number": mobile})
            users = frappe.get_all("User", filters={"mobile_no": mobile}, pluck="name")
            for u in users:
                if u != "Administrator":
                    frappe.delete_doc("User", u, ignore_permissions=True)
            
        frappe.db.commit()
        frappe.set_user("Administrator")

    def test_registration_success(self):
        frappe.form_dict.update({
            "first_name": "Test",
            "last_name": "User",
            "email": "test_auth_1@example.com",
            "mobile_no": "+919999900001",
            "password": "Password123!",
            "confirm_password": "Password123!"
        })
        
        response = register_endpoint()
        res_data = json.loads(response.get_data())
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(res_data.get("success"))
        self.assertEqual(res_data.get("user_id"), "test_auth_1@example.com")
        
        # Verify db records
        self.assertTrue(frappe.db.exists("User", "test_auth_1@example.com"))
        self.assertTrue(frappe.db.exists("CRM User Profile", {"user": "test_auth_1@example.com"}))
        
        # Verify default role is assigned
        roles = frappe.get_roles("test_auth_1@example.com")
        self.assertIn("Sales Executive", roles)

    def test_registration_validation(self):
        # 1. Non-matching password
        frappe.form_dict.update({
            "first_name": "Test",
            "email": "test_auth_2@example.com",
            "password": "Password123!",
            "confirm_password": "Password1234!"
        })
        response = register_endpoint()
        res_data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 400)
        self.assertFalse(res_data.get("success"))
        self.assertEqual(res_data.get("message"), "Password confirmation does not match")
        
        # 2. Weak password
        frappe.form_dict.update({
            "first_name": "Test",
            "email": "test_auth_2@example.com",
            "password": "weak",
            "confirm_password": "weak"
        })
        response = register_endpoint()
        res_data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 400)
        self.assertFalse(res_data.get("success"))
        self.assertIn("Password must be at least 12 characters", res_data.get("message"))

    def test_login_success_and_lockout(self):
        # Register a valid user
        frappe.form_dict.update({
            "first_name": "Test",
            "last_name": "User",
            "email": "test_auth_3@example.com",
            "mobile_no": "+919999900003",
            "password": "Password123!",
            "confirm_password": "Password123!"
        })
        register_endpoint()
        
        # 1. Login success
        frappe.form_dict.clear()
        frappe.form_dict.update({
            "email": "test_auth_3@example.com",
            "password": "Password123!"
        })
        response = login_endpoint()
        res_data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200, f"Login failed: {res_data.get('message') if isinstance(res_data, dict) else response.get_data()}")
        self.assertTrue(res_data.get("success"))
        self.assertTrue(res_data.get("token"))
        
        # 2. Login fail count & Lockout
        reset_failed_login("test_auth_3@example.com")
        frappe.form_dict.update({
            "email": "test_auth_3@example.com",
            "password": "WrongPassword!"
        })
        
        for _ in range(5):
            response = login_endpoint()
            
        # 6th attempt should be locked out
        self.assertTrue(is_account_locked("test_auth_3@example.com"))
        response = login_endpoint()
        res_data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 403)
        self.assertFalse(res_data.get("success"))
        self.assertIn("Account locked", res_data.get("message"))

    def test_profile_retrieval_and_update(self):
        # Register a valid user
        frappe.form_dict.update({
            "first_name": "Profile",
            "last_name": "Test",
            "email": "test_auth_2@example.com",
            "mobile_no": "+919999900002",
            "password": "Password123!",
            "confirm_password": "Password123!"
        })
        register_endpoint()
        
        # Authenticate as the user
        frappe.set_user("test_auth_2@example.com")
        
        # Get profile
        frappe.form_dict.clear()
        response = profile_endpoint()
        res_data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(res_data.get("success"))
        self.assertEqual(res_data.get("profile").get("email"), "test_auth_2@example.com")
        
        # Update profile
        frappe.local.request.method = "PUT"
        frappe.form_dict.update({
            "name": "Updated Name",
            "mobile": "+919999900009",
            "designation": "Sales Executive",
            "department": "Sales"
        })
        response = profile_endpoint()
        res_data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(res_data.get("success"))
        
        # Verify updates
        frappe.local.request.method = "GET"
        frappe.form_dict.clear()
        response = profile_endpoint()
        res_data = json.loads(response.get_data())
        self.assertEqual(res_data.get("profile").get("name"), "Updated Name")
        self.assertEqual(res_data.get("profile").get("mobile"), "+919999900009")

    def test_registration_guest_fails(self):
        frappe.set_user("Guest")
        frappe.form_dict.update({
            "first_name": "Test",
            "last_name": "User",
            "email": "test_auth_guest@example.com",
            "password": "Password123!",
            "confirm_password": "Password123!"
        })
        response = register_endpoint()
        res_data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 403)
        self.assertFalse(res_data.get("success"))
        self.assertIn("Permission denied", res_data.get("message"))

    def test_mobile_number_validation_rules(self):
        # Authenticate as admin to register new users
        frappe.set_user("Administrator")
        
        # Test valid numbers
        for num in ["+919876543210", "+918907654312"]:
            frappe.form_dict.clear()
            frappe.form_dict.update({
                "first_name": "Valid",
                "last_name": "User",
                "email": "test_valid_num@example.com",
                "mobile_no": num,
                "password": "Password123!",
                "confirm_password": "Password123!"
            })
            response = register_endpoint()
            res_data = json.loads(response.get_data())
            self.assertEqual(response.status_code, 200, f"Expected success for {num}, got {res_data.get('message')}")
            # Clean up user immediately to avoid duplicate errors in loop
            profile_name = frappe.db.get_value("CRM User Profile", {"user": "test_valid_num@example.com"})
            if profile_name:
                frappe.delete_doc("CRM User Profile", profile_name, ignore_permissions=True)
            frappe.delete_doc("User", "test_valid_num@example.com", ignore_permissions=True)
            frappe.db.commit()

        # Test invalid numbers
        invalid_numbers = ["9876543210", "+911234567890", "+91 9876543210", "abc123", "+91987654"]
        for num in invalid_numbers:
            frappe.form_dict.clear()
            frappe.form_dict.update({
                "first_name": "Invalid",
                "last_name": "User",
                "email": "test_invalid_num@example.com",
                "mobile_no": num,
                "password": "Password123!",
                "confirm_password": "Password123!"
            })
            # It should fail validation and raise a ValidationError returned as 500
            response = register_endpoint()
            res_data = json.loads(response.get_data())
            self.assertEqual(response.status_code, 500, f"Expected validation failure for {num}, but registered successfully")
            self.assertIn("Invalid mobile number format", res_data.get("message"))
            # Make sure user was not created
            self.assertFalse(frappe.db.exists("User", "test_invalid_num@example.com"))

    def test_duplicate_mobile_validation(self):
        # Register User A with a mobile number
        frappe.set_user("Administrator")
        frappe.form_dict.clear()
        frappe.form_dict.update({
            "first_name": "UserA",
            "email": "user_a@example.com",
            "mobile_no": "+919999900088",
            "password": "Password123!",
            "confirm_password": "Password123!"
        })
        resp1 = register_endpoint()
        self.assertEqual(resp1.status_code, 200)

        # Register User B with the SAME mobile number -> should fail at duplicate validation check
        frappe.form_dict.clear()
        frappe.form_dict.update({
            "first_name": "UserB",
            "email": "user_b@example.com",
            "mobile_no": "+919999900088",
            "password": "Password123!",
            "confirm_password": "Password123!"
        })
        resp2 = register_endpoint()
        res_data2 = json.loads(resp2.get_data())
        self.assertEqual(resp2.status_code, 400) # Duplicate check in endpoint returns 400
        self.assertIn("already exists", res_data2.get("message"))

        # Clean up User A
        profile_name = frappe.db.get_value("CRM User Profile", {"user": "user_a@example.com"}, "name")
        if profile_name:
            frappe.delete_doc("CRM User Profile", profile_name, ignore_permissions=True)
        frappe.delete_doc("User", "user_a@example.com", ignore_permissions=True)
        frappe.db.commit()

    def test_signup_role_escalation_prevention(self):
        from crm_pro.api_auth import signup_endpoint
        frappe.set_user("Guest")
        frappe.form_dict.clear()
        frappe.form_dict.update({
            "first_name": "TestEscalation",
            "email": "test_escalation@example.com",
            "contact": "+919999900009",
            "password": "Password123!",
            "role": "Admin"
        })
        res = signup_endpoint()
        self.assertEqual(res.get("success"), True)
        
        # Verify the created user has the base role "Sales Executive" but NOT "Admin"
        roles = frappe.get_roles("test_escalation@example.com")
        self.assertIn("Sales Executive", roles)
        self.assertNotIn("Admin", roles)
        
        # Clean up
        frappe.set_user("Administrator")
        profile_name = frappe.db.get_value("CRM User Profile", {"user": "test_escalation@example.com"}, "name")
        if profile_name:
            frappe.delete_doc("CRM User Profile", profile_name, ignore_permissions=True)
        frappe.delete_doc("User", "test_escalation@example.com", ignore_permissions=True)
        frappe.db.commit()

    def test_expired_session_bearer_token(self):
        from crm_pro.api_auth import check_bearer_token
        # Create a valid session
        user = "test_auth_3@example.com"
        # Make sure user exists
        if not frappe.db.exists("User", user):
            user_doc = frappe.get_doc({
                "doctype": "User",
                "email": user,
                "first_name": "TestToken",
                "enabled": 1
            })
            user_doc.insert(ignore_permissions=True)
            
        frappe.db.sql(
            "insert into tabSessions (user, sid, lastupdate, status) values (%s, %s, %s, %s)",
            (user, "test_sid_expired_bearer", frappe.utils.now_datetime(), "Active")
        )
        frappe.db.commit()
        
        # Set Authorization header in request mockup
        frappe.local.request.headers = {"Authorization": "Bearer test_sid_expired_bearer"}
        
        # Check bearer token - should set user to the test user
        check_bearer_token()
        self.assertEqual(frappe.session.user, user)
        
        # Modify lastupdate in DB to simulate expired session
        # Set it to 10 days ago (threshold is typically 1 hour to 1 day depending on session_expiry config)
        frappe.db.sql(
            "update tabSessions set lastupdate=%s where sid=%s",
            (frappe.utils.add_days(frappe.utils.now_datetime(), -10), "test_sid_expired_bearer")
        )
        frappe.db.commit()
        frappe.clear_cache()
        
        # Reset current session user
        frappe.session.user = "Guest"
        
        # Check bearer token - should NOT set user to the test user (it should remain Guest or raise Exception)
        check_bearer_token()
        self.assertEqual(frappe.session.user, "Guest")
        
        # Clean up
        frappe.set_user("Administrator")
        frappe.db.sql("delete from tabSessions where sid=%s", ("test_sid_expired_bearer",))
        frappe.db.commit()
