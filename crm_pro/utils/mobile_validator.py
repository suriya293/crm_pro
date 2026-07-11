import frappe
from frappe import _
import re

def validate_mobile(mobile):
    """
    Validates that a mobile number matches the E.164 standard without spaces, letters,
    or special characters except an optional leading plus, and has between 10 and 15 digits.
    """
    if not mobile:
        return
        
    # Strict E.164 Indian mobile format: +91 followed by a digit (6-9) and exactly 9 digits
    if not re.match(r"^\+91[6-9][0-9]{9}$", mobile):
        frappe.throw(
            _("Invalid mobile number format. Must start with +91, followed by a digit (6-9) and exactly 9 more digits. Spaces, alphabets, or special characters are not allowed (e.g. +919876543210)."),
            frappe.ValidationError
        )

def check_duplicate_mobile(mobile, email=None):
    """
    Verifies that a mobile number is not already assigned to another User (in tabUser.mobile_no)
    or another CRM User Profile (in phone_number). Comparisons are case-insensitive for email/user names.
    """
    if not mobile:
        return

    # Check tabUser for duplicates
    dup_users = frappe.get_all("User", filters={"mobile_no": mobile}, fields=["name"])
    for u in dup_users:
        if not email or u.name.lower() != email.lower():
            frappe.throw(
                _("A user with this mobile number already exists (User: {0})").format(u.name),
                frappe.LinkValidationError
            )

    # Check CRM User Profile for duplicates
    dup_profiles = frappe.get_all("CRM User Profile", filters={"phone_number": mobile}, fields=["name", "user"])
    for p in dup_profiles:
        if not email or (p.user and p.user.lower() != email.lower()):
            frappe.throw(
                _("A user with this mobile number already exists (Profile: {0})").format(p.user or p.name),
                frappe.LinkValidationError
            )

def validate_user_mobile(doc, method=None):
    """
    DocType validate hook for tabUser.
    """
    if doc.mobile_no:
        validate_mobile(doc.mobile_no)
        check_duplicate_mobile(doc.mobile_no, doc.name)

def validate_profile_mobile(doc, method=None):
    """
    DocType validate hook for CRM User Profile.
    """
    if doc.phone_number:
        validate_mobile(doc.phone_number)
        check_duplicate_mobile(doc.phone_number, doc.user)
