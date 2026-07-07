# CRM Pro Database Data Dictionary

## Table: tabCRM Activity (CRM Activity)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `activity_type` | VARCHAR(255) | Activity Type | Stores the activity type information. |
| `lead` | VARCHAR(255) | Associated Lead | Stores the associated lead information. |
| `deal` | VARCHAR(255) | Associated Deal | Stores the associated deal information. |
| `notes` | TEXT | Notes | Detailed notes, comments, or descriptions. |
| `activity_date` | DATETIME | Activity Date | Timestamp for process scheduling or historical tracking. |

---

## Table: tabCRM Attachment (CRM Attachment)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `lead` | VARCHAR(255) | Associated Lead | Stores the associated lead information. |
| `deal` | VARCHAR(255) | Associated Deal | Stores the associated deal information. |
| `file_url` | VARCHAR(255) | File Attachment | Stores the file attachment information. |
| `file_name` | VARCHAR(255) | File Name | Stores the name or identifier of the file name. |

---

## Table: tabCRM Audit Log (CRM Audit Log)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `ref_doctype` | VARCHAR(255) | Referenced DocType | Stores the referenced doctype information. |
| `ref_name` | VARCHAR(255) | Referenced ID | Stores the name or identifier of the referenced id. |
| `action` | VARCHAR(255) | Action Taken | Stores the action taken information. |
| `user` | VARCHAR(255) | User | Links to the User or agent responsible for this record. |
| `details` | TEXT | Audit Details | Stores the audit details information. |

---

## Table: tabCRM Call Log (CRM Call Log)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `lead` | VARCHAR(255) | Associated Lead | Stores the associated lead information. |
| `phone_number` | VARCHAR(255) | Phone Number | Phone or mobile contact number. |
| `duration_seconds` | INT(11) | Duration (Seconds) | Stores the duration (seconds) information. |
| `call_type` | VARCHAR(255) | Call Type | Stores the call type information. |
| `recording_url` | VARCHAR(255) | Recording URL | Stores the recording url information. |
| `summary` | TEXT | Summary | Stores the summary information. |

---

## Table: tabCRM Company (CRM Company)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `company_name` | VARCHAR(255) | Company Name | Stores the name or identifier of the company name. |
| `website` | VARCHAR(255) | Website | Stores the website information. |
| `industry` | VARCHAR(255) | Industry | Stores the industry information. |
| `employee_count` | INT(11) | Employee Count | Stores the employee count information. |
| `annual_revenue` | DECIMAL(21, 9) | Annual Revenue | Financial value or monetary amount associated with this entry. |
| `address` | TEXT | Address | Stores the address information. |

---

## Table: tabCRM Contact (CRM Contact)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `contact_name` | VARCHAR(255) | Contact Name | Stores the name or identifier of the contact name. |
| `company` | VARCHAR(255) | Company | Stores the company information. |
| `lead` | VARCHAR(255) | Associated Lead | Stores the associated lead information. |
| `job_title` | VARCHAR(255) | Job Title | Stores the job title information. |
| `phones` | Child Table Link | Phone Numbers | Phone or mobile contact number. |
| `emails` | Child Table Link | Email Addresses | Email address for notifications and correspondence. |
| `history_summary` | TEXT | Contact History Summary | Stores the contact history summary information. |

---

## Table: tabCRM Contact Email (CRM Contact Email)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `email` | VARCHAR(255) | Email Address | Email address for notifications and correspondence. |
| `type` | VARCHAR(255) | Type | Stores the type information. |

---

## Table: tabCRM Contact Phone (CRM Contact Phone)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `phone` | VARCHAR(255) | Phone Number | Phone or mobile contact number. |
| `type` | VARCHAR(255) | Type | Stores the type information. |

---

## Table: tabCRM Custom Field (CRM Custom Field)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `field_name` | VARCHAR(255) | Field Name | Stores the name or identifier of the field name. |
| `field_value` | VARCHAR(255) | Field Value | Financial value or monetary amount associated with this entry. |

---

## Table: tabCRM Dashboard Metrics (CRM Dashboard Metrics)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `metric_date` | DATE | Metric Date | Timestamp for process scheduling or historical tracking. |
| `total_leads` | INT(11) | Total Leads | Stores the total leads information. |
| `new_leads` | INT(11) | New Leads | Stores the new leads information. |
| `converted_leads` | INT(11) | Converted Leads | Stores the converted leads information. |
| `won_deals` | INT(11) | Won Deals | Stores the won deals information. |
| `lost_deals` | INT(11) | Lost Deals | Stores the lost deals information. |
| `total_revenue` | DECIMAL(21, 9) | Total Revenue | Financial value or monetary amount associated with this entry. |

---

## Table: tabCRM Deal (CRM Deal)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `deal_name` | VARCHAR(255) | Deal Name | Stores the name or identifier of the deal name. |
| `lead` | VARCHAR(255) | Lead Source | Stores the lead source information. |
| `company` | VARCHAR(255) | Company | Stores the company information. |
| `deal_stage` | VARCHAR(255) | Deal Stage | Defines the pipeline or process stage of this entity. |
| `deal_value` | DECIMAL(21, 9) | Deal Value | Financial value or monetary amount associated with this entry. |
| `expected_close` | DATE | Expected Close Date | Stores the expected close date information. |
| `forecast_category` | VARCHAR(255) | Forecast Category | Stores the forecast category information. |
| `deal_status` | VARCHAR(255) | Deal Status | Tracks the current lifecycle status of this record. |

---

## Table: tabCRM Email Log (CRM Email Log)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `lead` | VARCHAR(255) | Associated Lead | Stores the associated lead information. |
| `sender` | VARCHAR(255) | Sender | Stores the sender information. |
| `recipient` | VARCHAR(255) | Recipient | Stores the recipient information. |
| `subject` | VARCHAR(255) | Subject | Stores the subject information. |
| `body` | TEXT | Body Content | Stores the body content information. |
| `sent_received` | VARCHAR(255) | Direction | Stores the direction information. |

---

## Table: tabCRM Lead (CRM Lead)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `lead_name` | VARCHAR(255) | Lead Name | Stores the name or identifier of the lead name. |
| `email` | VARCHAR(255) | Email | Email address for notifications and correspondence. |
| `mobile` | VARCHAR(255) | Mobile | Phone or mobile contact number. |
| `country_code` | VARCHAR(255) | Country Code | Stores the country code information. |
| `stage` | VARCHAR(255) | Stage | Defines the pipeline or process stage of this entity. |
| `source` | VARCHAR(255) | Source | Stores the source information. |
| `user` | VARCHAR(255) | User | Links to the User or agent responsible for this record. |
| `priority` | VARCHAR(255) | Priority | Stores the priority information. |
| `segment` | VARCHAR(255) | Segment | Stores the segment information. |
| `alt_mobile_1` | VARCHAR(255) | Alternate Mobile 1 | Phone or mobile contact number. |
| `alt_mobile_2` | VARCHAR(255) | Alternate Mobile 2 | Phone or mobile contact number. |
| `alt_mobile_3` | VARCHAR(255) | Alternate Mobile 3 | Phone or mobile contact number. |
| `age` | INT(11) | Age | Stores the age information. |
| `gender` | VARCHAR(255) | Gender | Stores the gender information. |
| `address` | TEXT | Address | Stores the address information. |
| `state` | VARCHAR(255) | State | Stores the state information. |
| `city` | VARCHAR(255) | City | Stores the city information. |
| `country` | VARCHAR(255) | Country | Stores the country information. |
| `pincode` | VARCHAR(255) | Pincode | Stores the pincode information. |
| `company_name` | VARCHAR(255) | Company Name | Stores the name or identifier of the company name. |
| `designation` | VARCHAR(255) | Designation | Stores the designation information. |
| `website` | VARCHAR(255) | Website | Stores the website information. |
| `tags` | VARCHAR(255) | Tags | Stores the tags information. |
| `opportunity_value` | DECIMAL(21, 9) | Opportunity Value | Financial value or monetary amount associated with this entry. |
| `followup_date` | DATETIME | Follow-up Date | Timestamp for process scheduling or historical tracking. |
| `custom_fields` | Child Table Link | Custom Fields | Stores the custom fields information. |

---

## Table: tabCRM Lead Snapshot (CRM Lead Snapshot)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `snapshot_date` | DATE | Snapshot Date | Timestamp for process scheduling or historical tracking. |
| `total_leads` | INT(11) | Total Leads | Stores the total leads information. |
| `active_leads` | INT(11) | Active Leads | Stores the active leads information. |
| `converted_leads` | INT(11) | Converted Leads | Stores the converted leads information. |
| `conversion_rate` | DECIMAL(21, 9) | Conversion Rate | Stores the conversion rate information. |

---

## Table: tabCRM Meeting (CRM Meeting)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `meeting_subject` | VARCHAR(255) | Meeting Subject | Stores the meeting subject information. |
| `lead` | VARCHAR(255) | Associated Lead | Stores the associated lead information. |
| `meeting_time` | DATETIME | Meeting Time | Timestamp for process scheduling or historical tracking. |
| `location` | VARCHAR(255) | Location | Stores the location information. |
| `agenda` | TEXT | Agenda | Stores the agenda information. |

---

## Table: tabCRM Note (CRM Note)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `lead` | VARCHAR(255) | Associated Lead | Stores the associated lead information. |
| `deal` | VARCHAR(255) | Associated Deal | Stores the associated deal information. |
| `content` | TEXT | Note Content | Stores the note content information. |
| `added_by` | VARCHAR(255) | Added By | Stores the added by information. |

---

## Table: tabCRM Notification (CRM Notification)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `notification_title` | VARCHAR(255) | Notification Title | Stores the notification title information. |
| `message` | TEXT | Message Content | Stores the message content information. |
| `for_user` | VARCHAR(255) | For User | Links to the User or agent responsible for this record. |
| `is_read` | INT(11) | Is Read | Stores the is read information. |

---

## Table: tabCRM Pipeline (CRM Pipeline)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `pipeline_name` | VARCHAR(255) | Pipeline Name | Stores the name or identifier of the pipeline name. |
| `description` | TEXT | Description | Detailed notes, comments, or descriptions. |

---

## Table: tabCRM Pipeline Stage (CRM Pipeline Stage)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `stage_name` | VARCHAR(255) | Stage Name | Stores the name or identifier of the stage name. |
| `pipeline` | VARCHAR(255) | Pipeline | Stores the pipeline information. |
| `order` | INT(11) | Order | Stores the order information. |
| `color` | VARCHAR(255) | Color Hex | Stores the color hex information. |

---

## Table: tabCRM Reminder (CRM Reminder)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `reminder_subject` | VARCHAR(255) | Reminder Subject | Stores the reminder subject information. |
| `lead` | VARCHAR(255) | Associated Lead | Stores the associated lead information. |
| `reminder_time` | DATETIME | Reminder Time | Timestamp for process scheduling or historical tracking. |
| `is_sent` | INT(11) | Is Sent | Stores the is sent information. |
| `recipient` | VARCHAR(255) | Recipient | Stores the recipient information. |

---

## Table: tabCRM Role Configuration (CRM Role Configuration)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `role_name` | VARCHAR(255) | Role Name | Stores the name or identifier of the role name. |
| `allowed_views` | TEXT | Allowed Views | Stores the allowed views information. |
| `allowed_actions` | TEXT | Allowed Actions | Stores the allowed actions information. |

---

## Table: tabCRM Sales Target (CRM Sales Target)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `target_name` | VARCHAR(255) | Target Name | Stores the name or identifier of the target name. |
| `target_type` | VARCHAR(255) | Target Type | Stores the target type information. |
| `user` | VARCHAR(255) | User | Links to the User or agent responsible for this record. |
| `team` | VARCHAR(255) | Team | Stores the team information. |
| `target_value` | DECIMAL(21, 9) | Target Value | Financial value or monetary amount associated with this entry. |
| `achieved_value` | DECIMAL(21, 9) | Achieved Value | Financial value or monetary amount associated with this entry. |
| `fiscal_year` | VARCHAR(255) | Fiscal Year | Stores the fiscal year information. |

---

## Table: tabCRM Settings (CRM Settings)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `company_name` | VARCHAR(255) | Company Name | Stores the name or identifier of the company name. |
| `default_pipeline` | VARCHAR(255) | Default Pipeline | Stores the default pipeline information. |
| `enable_ai_suggestions` | INT(11) | Enable AI Suggestions | Stores the enable ai suggestions information. |
| `enable_whatsapp_integration` | INT(11) | Enable WhatsApp Integration | Stores the enable whatsapp integration information. |
| `whatsapp_access_token` | VARCHAR(255) | WhatsApp Access Token | Stores the whatsapp access token information. |
| `whatsapp_phone_number_id` | VARCHAR(255) | WhatsApp Phone Number ID | Phone or mobile contact number. |
| `facebook_access_token` | VARCHAR(255) | Facebook Access Token | Stores the facebook access token information. |
| `facebook_webhook_verify_token` | VARCHAR(255) | Facebook Webhook Verify Token | Stores the facebook webhook verify token information. |
| `facebook_app_secret` | VARCHAR(255) | Facebook App Secret | Stores the facebook app secret information. |

---

## Table: tabCRM Task (CRM Task)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `task_subject` | VARCHAR(255) | Task Subject | Stores the task subject information. |
| `lead` | VARCHAR(255) | Associated Lead | Stores the associated lead information. |
| `deal` | VARCHAR(255) | Associated Deal | Stores the associated deal information. |
| `due_date` | DATE | Due Date | Timestamp for process scheduling or historical tracking. |
| `status` | VARCHAR(255) | Status | Tracks the current lifecycle status of this record. |
| `assigned_to` | VARCHAR(255) | Assigned To | Links to the User or agent responsible for this record. |

---

## Table: tabCRM Team (CRM Team)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `team_name` | VARCHAR(255) | Team Name | Stores the name or identifier of the team name. |
| `lead_user` | VARCHAR(255) | Team Lead | Links to the User or agent responsible for this record. |
| `description` | TEXT | Description | Detailed notes, comments, or descriptions. |

---

## Table: tabCRM User Profile (CRM User Profile)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `user` | VARCHAR(255) | User Link | Links to the User or agent responsible for this record. |
| `phone_number` | VARCHAR(255) | Phone Number | Phone or mobile contact number. |
| `profile_picture` | VARCHAR(255) | Profile Picture | Stores the profile picture information. |
| `designation` | VARCHAR(255) | Designation | Stores the designation information. |
| `team` | VARCHAR(255) | Associated Team | Stores the associated team information. |

---

## Table: tabCRM WhatsApp Log (CRM WhatsApp Log)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `lead` | VARCHAR(255) | Associated Lead | Stores the associated lead information. |
| `phone_number` | VARCHAR(255) | Phone Number | Phone or mobile contact number. |
| `message` | TEXT | Message Content | Stores the message content information. |
| `direction` | VARCHAR(255) | Direction | Stores the direction information. |

---

## Table: tabactivity (activity)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `activity_type` | VARCHAR(255) | Activity Type | Stores the activity type information. |
| `lead` | VARCHAR(255) | Lead | Stores the lead information. |
| `description` | TEXT | Description | Detailed notes, comments, or descriptions. |
| `timestamp` | DATETIME | Timestamp | Timestamp for process scheduling or historical tracking. |
| `performed_by` | VARCHAR(255) | Performed By | Stores the performed by information. |
| `owner` | VARCHAR(255) | Owner | Links to the User or agent responsible for this record. |
| `assigned_to` | VARCHAR(255) | Assigned To | Links to the User or agent responsible for this record. |
| `created_by` | VARCHAR(255) | Created By | Stores the created by information. |
| `modified_by` | VARCHAR(255) | Modified By | Stores the modified by information. |
| `creation` | DATETIME | Creation | Timestamp for process scheduling or historical tracking. |
| `modified` | DATETIME | Modified | Timestamp for process scheduling or historical tracking. |
| `docstatus` | VARCHAR(255) | Docstatus | Tracks the current lifecycle status of this record. |
| `company` | VARCHAR(255) | Company | Stores the company information. |
| `territory` | VARCHAR(255) | Territory | Stores the territory information. |
| `team` | VARCHAR(255) | Team | Stores the team information. |

---

## Table: tabapi_log (api_log)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `endpoint` | VARCHAR(255) | Endpoint | Stores the endpoint information. |
| `method` | VARCHAR(255) | Method | Stores the method information. |
| `ip_address` | VARCHAR(255) | IP Address | Stores the ip address information. |
| `user` | VARCHAR(255) | User | Links to the User or agent responsible for this record. |
| `status` | VARCHAR(255) | Status | Tracks the current lifecycle status of this record. |
| `owner` | VARCHAR(255) | Owner | Links to the User or agent responsible for this record. |
| `assigned_to` | VARCHAR(255) | Assigned To | Links to the User or agent responsible for this record. |
| `created_by` | VARCHAR(255) | Created By | Stores the created by information. |
| `modified_by` | VARCHAR(255) | Modified By | Stores the modified by information. |
| `creation` | DATETIME | Creation | Timestamp for process scheduling or historical tracking. |
| `modified` | DATETIME | Modified | Timestamp for process scheduling or historical tracking. |
| `docstatus` | VARCHAR(255) | Docstatus | Tracks the current lifecycle status of this record. |

---

## Table: tabaudit_log (audit_log)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `action` | VARCHAR(255) | Action | Stores the action information. |
| `details` | TEXT | Details | Stores the details information. |
| `user` | VARCHAR(255) | User | Links to the User or agent responsible for this record. |
| `timestamp` | DATETIME | Timestamp | Timestamp for process scheduling or historical tracking. |
| `owner` | VARCHAR(255) | Owner | Links to the User or agent responsible for this record. |
| `assigned_to` | VARCHAR(255) | Assigned To | Links to the User or agent responsible for this record. |
| `created_by` | VARCHAR(255) | Created By | Stores the created by information. |
| `modified_by` | VARCHAR(255) | Modified By | Stores the modified by information. |
| `creation` | DATETIME | Creation | Timestamp for process scheduling or historical tracking. |
| `modified` | DATETIME | Modified | Timestamp for process scheduling or historical tracking. |
| `docstatus` | VARCHAR(255) | Docstatus | Tracks the current lifecycle status of this record. |

---

## Table: tabautomation_rule (automation_rule)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `rule_name` | VARCHAR(255) | Rule Name | Stores the name or identifier of the rule name. |
| `trigger_event` | VARCHAR(255) | Trigger Event | Stores the trigger event information. |
| `target_doctype` | VARCHAR(255) | Target DocType | Stores the target doctype information. |
| `action` | TEXT | Action | Stores the action information. |
| `is_active` | INT(11) | Is Active | Stores the is active information. |
| `owner` | VARCHAR(255) | Owner | Links to the User or agent responsible for this record. |
| `assigned_to` | VARCHAR(255) | Assigned To | Links to the User or agent responsible for this record. |
| `created_by` | VARCHAR(255) | Created By | Stores the created by information. |
| `modified_by` | VARCHAR(255) | Modified By | Stores the modified by information. |
| `creation` | DATETIME | Creation | Timestamp for process scheduling or historical tracking. |
| `modified` | DATETIME | Modified | Timestamp for process scheduling or historical tracking. |
| `docstatus` | VARCHAR(255) | Docstatus | Tracks the current lifecycle status of this record. |

---

## Table: tabcampaign (campaign)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `campaign_name` | VARCHAR(255) | Campaign Name | Stores the name or identifier of the campaign name. |
| `start_date` | DATE | Start Date | Timestamp for process scheduling or historical tracking. |
| `end_date` | DATE | End Date | Timestamp for process scheduling or historical tracking. |
| `budget` | DECIMAL(21, 9) | Budget | Stores the budget information. |
| `target_audience` | VARCHAR(255) | Target Audience | Stores the target audience information. |
| `status` | VARCHAR(255) | Status | Tracks the current lifecycle status of this record. |
| `owner` | VARCHAR(255) | Owner | Links to the User or agent responsible for this record. |
| `assigned_to` | VARCHAR(255) | Assigned To | Links to the User or agent responsible for this record. |
| `created_by` | VARCHAR(255) | Created By | Stores the created by information. |
| `modified_by` | VARCHAR(255) | Modified By | Stores the modified by information. |
| `creation` | DATETIME | Creation | Timestamp for process scheduling or historical tracking. |
| `modified` | DATETIME | Modified | Timestamp for process scheduling or historical tracking. |
| `docstatus` | VARCHAR(255) | Docstatus | Tracks the current lifecycle status of this record. |
| `company` | VARCHAR(255) | Company | Stores the company information. |
| `territory` | VARCHAR(255) | Territory | Stores the territory information. |
| `team` | VARCHAR(255) | Team | Stores the team information. |

---

## Table: tabcompany (company)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `company_name` | VARCHAR(255) | Company Name | Stores the name or identifier of the company name. |
| `address` | TEXT | Address | Stores the address information. |
| `industry` | VARCHAR(255) | Industry | Stores the industry information. |
| `website` | VARCHAR(255) | Website | Stores the website information. |
| `account_manager` | VARCHAR(255) | Account Manager | Stores the account manager information. |
| `owner` | VARCHAR(255) | Owner | Links to the User or agent responsible for this record. |
| `assigned_to` | VARCHAR(255) | Assigned To | Links to the User or agent responsible for this record. |
| `created_by` | VARCHAR(255) | Created By | Stores the created by information. |
| `modified_by` | VARCHAR(255) | Modified By | Stores the modified by information. |
| `creation` | DATETIME | Creation | Timestamp for process scheduling or historical tracking. |
| `modified` | DATETIME | Modified | Timestamp for process scheduling or historical tracking. |
| `docstatus` | VARCHAR(255) | Docstatus | Tracks the current lifecycle status of this record. |
| `company` | VARCHAR(255) | Company | Stores the company information. |
| `territory` | VARCHAR(255) | Territory | Stores the territory information. |
| `team` | VARCHAR(255) | Team | Stores the team information. |

---

## Table: tabcontact (contact)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `contact_name` | VARCHAR(255) | Contact Name | Stores the name or identifier of the contact name. |
| `first_name` | VARCHAR(255) | First Name | Stores the name or identifier of the first name. |
| `last_name` | VARCHAR(255) | Last Name | Stores the name or identifier of the last name. |
| `email` | VARCHAR(255) | Email | Email address for notifications and correspondence. |
| `mobile_no` | VARCHAR(255) | Mobile Number | Phone or mobile contact number. |
| `associated_lead` | VARCHAR(255) | Lead | Stores the lead information. |
| `company` | VARCHAR(255) | Company | Stores the company information. |
| `role` | VARCHAR(255) | Role | Stores the role information. |
| `created_at` | DATETIME | Created At | Stores the created at information. |
| `updated_at` | DATETIME | Updated At | Timestamp for process scheduling or historical tracking. |

---

## Table: tabdeal (deal)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `deal_name` | VARCHAR(255) | Deal Name | Stores the name or identifier of the deal name. |
| `opportunity` | VARCHAR(255) | Opportunity | Stores the opportunity information. |
| `amount` | DECIMAL(21, 9) | Amount | Financial value or monetary amount associated with this entry. |
| `stage` | VARCHAR(255) | Stage | Defines the pipeline or process stage of this entity. |
| `expected_close_date` | DATE | Expected Close Date | Timestamp for process scheduling or historical tracking. |
| `owner` | VARCHAR(255) | Owner | Links to the User or agent responsible for this record. |
| `assigned_to` | VARCHAR(255) | Assigned To | Links to the User or agent responsible for this record. |
| `created_by` | VARCHAR(255) | Created By | Stores the created by information. |
| `modified_by` | VARCHAR(255) | Modified By | Stores the modified by information. |
| `creation` | DATETIME | Creation | Timestamp for process scheduling or historical tracking. |
| `modified` | DATETIME | Modified | Timestamp for process scheduling or historical tracking. |
| `docstatus` | VARCHAR(255) | Docstatus | Tracks the current lifecycle status of this record. |
| `company` | VARCHAR(255) | Company | Stores the company information. |
| `territory` | VARCHAR(255) | Territory | Stores the territory information. |
| `team` | VARCHAR(255) | Team | Stores the team information. |

---

## Table: tabdepartment (department)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `department_name` | VARCHAR(255) | Department Name | Stores the name or identifier of the department name. |
| `owner` | VARCHAR(255) | Owner | Links to the User or agent responsible for this record. |
| `assigned_to` | VARCHAR(255) | Assigned To | Links to the User or agent responsible for this record. |
| `created_by` | VARCHAR(255) | Created By | Stores the created by information. |
| `modified_by` | VARCHAR(255) | Modified By | Stores the modified by information. |
| `creation` | DATETIME | Creation | Timestamp for process scheduling or historical tracking. |
| `modified` | DATETIME | Modified | Timestamp for process scheduling or historical tracking. |
| `docstatus` | VARCHAR(255) | Docstatus | Tracks the current lifecycle status of this record. |
| `company` | VARCHAR(255) | Company | Stores the company information. |

---

## Table: tabexport_job (export_job)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `doctype_to_export` | VARCHAR(255) | DocType to Export | Stores the doctype to export information. |
| `file_path` | VARCHAR(255) | File Path | Stores the file path information. |
| `status` | VARCHAR(255) | Status | Tracks the current lifecycle status of this record. |
| `owner` | VARCHAR(255) | Owner | Links to the User or agent responsible for this record. |
| `assigned_to` | VARCHAR(255) | Assigned To | Links to the User or agent responsible for this record. |
| `created_by` | VARCHAR(255) | Created By | Stores the created by information. |
| `modified_by` | VARCHAR(255) | Modified By | Stores the modified by information. |
| `creation` | DATETIME | Creation | Timestamp for process scheduling or historical tracking. |
| `modified` | DATETIME | Modified | Timestamp for process scheduling or historical tracking. |
| `docstatus` | VARCHAR(255) | Docstatus | Tracks the current lifecycle status of this record. |

---

## Table: tabfacebook_lead (facebook_lead)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `facebook_lead_id` | VARCHAR(255) | Facebook Lead ID | Stores the facebook lead id information. |
| `form_name` | VARCHAR(255) | Form Name | Stores the name or identifier of the form name. |
| `campaign` | VARCHAR(255) | Campaign | Stores the campaign information. |
| `lead_info` | TEXT | Lead Info | Stores the lead info information. |
| `sync_status` | VARCHAR(255) | Sync Status | Tracks the current lifecycle status of this record. |
| `owner` | VARCHAR(255) | Owner | Links to the User or agent responsible for this record. |
| `assigned_to` | VARCHAR(255) | Assigned To | Links to the User or agent responsible for this record. |
| `created_by` | VARCHAR(255) | Created By | Stores the created by information. |
| `modified_by` | VARCHAR(255) | Modified By | Stores the modified by information. |
| `creation` | DATETIME | Creation | Timestamp for process scheduling or historical tracking. |
| `modified` | DATETIME | Modified | Timestamp for process scheduling or historical tracking. |
| `docstatus` | VARCHAR(255) | Docstatus | Tracks the current lifecycle status of this record. |
| `company` | VARCHAR(255) | Company | Stores the company information. |
| `territory` | VARCHAR(255) | Territory | Stores the territory information. |
| `team` | VARCHAR(255) | Team | Stores the team information. |

---

## Table: tabfollowup (followup)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `followup_date` | DATE | Follow‑up Date | Timestamp for process scheduling or historical tracking. |
| `lead` | VARCHAR(255) | Lead | Stores the lead information. |
| `notes` | TEXT | Notes | Detailed notes, comments, or descriptions. |
| `outcome` | VARCHAR(255) | Outcome | Stores the outcome information. |
| `next_step` | VARCHAR(255) | Next Step | Stores the next step information. |
| `owner` | VARCHAR(255) | Owner | Links to the User or agent responsible for this record. |
| `assigned_to` | VARCHAR(255) | Assigned To | Links to the User or agent responsible for this record. |
| `created_by` | VARCHAR(255) | Created By | Stores the created by information. |
| `modified_by` | VARCHAR(255) | Modified By | Stores the modified by information. |
| `creation` | DATETIME | Creation | Timestamp for process scheduling or historical tracking. |
| `modified` | DATETIME | Modified | Timestamp for process scheduling or historical tracking. |
| `docstatus` | VARCHAR(255) | Docstatus | Tracks the current lifecycle status of this record. |
| `company` | VARCHAR(255) | Company | Stores the company information. |
| `territory` | VARCHAR(255) | Territory | Stores the territory information. |
| `team` | VARCHAR(255) | Team | Stores the team information. |

---

## Table: tabimport_job (import_job)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `file_path` | VARCHAR(255) | File Path | Stores the file path information. |
| `doctype_to_import` | VARCHAR(255) | DocType to Import | Stores the doctype to import information. |
| `status` | VARCHAR(255) | Status | Tracks the current lifecycle status of this record. |
| `owner` | VARCHAR(255) | Owner | Links to the User or agent responsible for this record. |
| `assigned_to` | VARCHAR(255) | Assigned To | Links to the User or agent responsible for this record. |
| `created_by` | VARCHAR(255) | Created By | Stores the created by information. |
| `modified_by` | VARCHAR(255) | Modified By | Stores the modified by information. |
| `creation` | DATETIME | Creation | Timestamp for process scheduling or historical tracking. |
| `modified` | DATETIME | Modified | Timestamp for process scheduling or historical tracking. |
| `docstatus` | VARCHAR(255) | Docstatus | Tracks the current lifecycle status of this record. |

---

## Table: tabinvoice (invoice)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `customer` | VARCHAR(255) | Customer | Stores the customer information. |
| `posting_date` | DATE | Posting Date | Timestamp for process scheduling or historical tracking. |
| `status` | VARCHAR(255) | Status | Tracks the current lifecycle status of this record. |
| `grand_total` | DECIMAL(21, 9) | Grand Total | Stores the grand total information. |
| `owner` | VARCHAR(255) | Owner | Links to the User or agent responsible for this record. |
| `assigned_to` | VARCHAR(255) | Assigned To | Links to the User or agent responsible for this record. |
| `created_by` | VARCHAR(255) | Created By | Stores the created by information. |
| `modified_by` | VARCHAR(255) | Modified By | Stores the modified by information. |
| `creation` | DATETIME | Creation | Timestamp for process scheduling or historical tracking. |
| `modified` | DATETIME | Modified | Timestamp for process scheduling or historical tracking. |
| `docstatus` | VARCHAR(255) | Docstatus | Tracks the current lifecycle status of this record. |
| `company` | VARCHAR(255) | Company | Stores the company information. |
| `territory` | VARCHAR(255) | Territory | Stores the territory information. |
| `team` | VARCHAR(255) | Team | Stores the team information. |

---

## Table: tablead (lead)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `lead_name` | VARCHAR(255) | Lead Name | Stores the name or identifier of the lead name. |
| `lead_source` | VARCHAR(255) | Lead Source | Stores the lead source information. |
| `mobile_no` | VARCHAR(255) | Mobile Number | Phone or mobile contact number. |
| `email` | VARCHAR(255) | Email | Email address for notifications and correspondence. |
| `status` | VARCHAR(255) | Status | Tracks the current lifecycle status of this record. |
| `assigned_to` | VARCHAR(255) | Assigned To | Links to the User or agent responsible for this record. |
| `created_at` | DATETIME | Created At | Stores the created at information. |
| `updated_at` | DATETIME | Updated At | Timestamp for process scheduling or historical tracking. |

---

## Table: tablead_source (lead_source)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `source_name` | VARCHAR(255) | Source Name | Stores the name or identifier of the source name. |
| `owner` | VARCHAR(255) | Owner | Links to the User or agent responsible for this record. |
| `assigned_to` | VARCHAR(255) | Assigned To | Links to the User or agent responsible for this record. |
| `created_by` | VARCHAR(255) | Created By | Stores the created by information. |
| `modified_by` | VARCHAR(255) | Modified By | Stores the modified by information. |
| `creation` | DATETIME | Creation | Timestamp for process scheduling or historical tracking. |
| `modified` | DATETIME | Modified | Timestamp for process scheduling or historical tracking. |
| `docstatus` | VARCHAR(255) | Docstatus | Tracks the current lifecycle status of this record. |
| `company` | VARCHAR(255) | Company | Stores the company information. |
| `territory` | VARCHAR(255) | Territory | Stores the territory information. |
| `team` | VARCHAR(255) | Team | Stores the team information. |

---

## Table: tabnotification (notification)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `subject` | VARCHAR(255) | Subject | Stores the subject information. |
| `message` | TEXT | Message | Stores the message information. |
| `for_user` | VARCHAR(255) | For User | Links to the User or agent responsible for this record. |
| `is_read` | INT(11) | Is Read | Stores the is read information. |
| `owner` | VARCHAR(255) | Owner | Links to the User or agent responsible for this record. |
| `assigned_to` | VARCHAR(255) | Assigned To | Links to the User or agent responsible for this record. |
| `created_by` | VARCHAR(255) | Created By | Stores the created by information. |
| `modified_by` | VARCHAR(255) | Modified By | Stores the modified by information. |
| `creation` | DATETIME | Creation | Timestamp for process scheduling or historical tracking. |
| `modified` | DATETIME | Modified | Timestamp for process scheduling or historical tracking. |
| `docstatus` | VARCHAR(255) | Docstatus | Tracks the current lifecycle status of this record. |

---

## Table: tabopportunity (opportunity)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `opportunity_name` | VARCHAR(255) | Opportunity Name | Stores the name or identifier of the opportunity name. |
| `lead` | VARCHAR(255) | Lead | Stores the lead information. |
| `value` | DECIMAL(21, 9) | Value | Financial value or monetary amount associated with this entry. |
| `probability` | INT(11) | Probability | Stores the probability information. |
| `expected_closure` | DATE | Expected Closure | Stores the expected closure information. |
| `status` | VARCHAR(255) | Status | Tracks the current lifecycle status of this record. |
| `owner` | VARCHAR(255) | Owner | Links to the User or agent responsible for this record. |
| `assigned_to` | VARCHAR(255) | Assigned To | Links to the User or agent responsible for this record. |
| `created_by` | VARCHAR(255) | Created By | Stores the created by information. |
| `modified_by` | VARCHAR(255) | Modified By | Stores the modified by information. |
| `creation` | DATETIME | Creation | Timestamp for process scheduling or historical tracking. |
| `modified` | DATETIME | Modified | Timestamp for process scheduling or historical tracking. |
| `docstatus` | VARCHAR(255) | Docstatus | Tracks the current lifecycle status of this record. |
| `company` | VARCHAR(255) | Company | Stores the company information. |
| `territory` | VARCHAR(255) | Territory | Stores the territory information. |
| `team` | VARCHAR(255) | Team | Stores the team information. |

---

## Table: tabpayment_entry (payment_entry)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `invoice` | VARCHAR(255) | Invoice | Stores the invoice information. |
| `amount` | DECIMAL(21, 9) | Amount | Financial value or monetary amount associated with this entry. |
| `payment_date` | DATE | Payment Date | Timestamp for process scheduling or historical tracking. |
| `status` | VARCHAR(255) | Status | Tracks the current lifecycle status of this record. |
| `owner` | VARCHAR(255) | Owner | Links to the User or agent responsible for this record. |
| `assigned_to` | VARCHAR(255) | Assigned To | Links to the User or agent responsible for this record. |
| `created_by` | VARCHAR(255) | Created By | Stores the created by information. |
| `modified_by` | VARCHAR(255) | Modified By | Stores the modified by information. |
| `creation` | DATETIME | Creation | Timestamp for process scheduling or historical tracking. |
| `modified` | DATETIME | Modified | Timestamp for process scheduling or historical tracking. |
| `docstatus` | VARCHAR(255) | Docstatus | Tracks the current lifecycle status of this record. |
| `company` | VARCHAR(255) | Company | Stores the company information. |
| `territory` | VARCHAR(255) | Territory | Stores the territory information. |
| `team` | VARCHAR(255) | Team | Stores the team information. |

---

## Table: tabprice_list (price_list)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `price_list_name` | VARCHAR(255) | Price List Name | Stores the name or identifier of the price list name. |
| `product` | VARCHAR(255) | Product | Stores the product information. |
| `price` | DECIMAL(21, 9) | Price | Financial value or monetary amount associated with this entry. |
| `owner` | VARCHAR(255) | Owner | Links to the User or agent responsible for this record. |
| `assigned_to` | VARCHAR(255) | Assigned To | Links to the User or agent responsible for this record. |
| `created_by` | VARCHAR(255) | Created By | Stores the created by information. |
| `modified_by` | VARCHAR(255) | Modified By | Stores the modified by information. |
| `creation` | DATETIME | Creation | Timestamp for process scheduling or historical tracking. |
| `modified` | DATETIME | Modified | Timestamp for process scheduling or historical tracking. |
| `docstatus` | VARCHAR(255) | Docstatus | Tracks the current lifecycle status of this record. |
| `company` | VARCHAR(255) | Company | Stores the company information. |
| `territory` | VARCHAR(255) | Territory | Stores the territory information. |
| `team` | VARCHAR(255) | Team | Stores the team information. |

---

## Table: tabproduct (product)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `product_name` | VARCHAR(255) | Product Name | Stores the name or identifier of the product name. |
| `product_category` | VARCHAR(255) | Product Category | Stores the product category information. |
| `is_active` | INT(11) | Is Active | Stores the is active information. |
| `description` | TEXT | Description | Detailed notes, comments, or descriptions. |
| `owner` | VARCHAR(255) | Owner | Links to the User or agent responsible for this record. |
| `assigned_to` | VARCHAR(255) | Assigned To | Links to the User or agent responsible for this record. |
| `created_by` | VARCHAR(255) | Created By | Stores the created by information. |
| `modified_by` | VARCHAR(255) | Modified By | Stores the modified by information. |
| `creation` | DATETIME | Creation | Timestamp for process scheduling or historical tracking. |
| `modified` | DATETIME | Modified | Timestamp for process scheduling or historical tracking. |
| `docstatus` | VARCHAR(255) | Docstatus | Tracks the current lifecycle status of this record. |
| `company` | VARCHAR(255) | Company | Stores the company information. |
| `territory` | VARCHAR(255) | Territory | Stores the territory information. |
| `team` | VARCHAR(255) | Team | Stores the team information. |

---

## Table: tabproduct_category (product_category)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `category_name` | VARCHAR(255) | Category Name | Stores the name or identifier of the category name. |
| `owner` | VARCHAR(255) | Owner | Links to the User or agent responsible for this record. |
| `assigned_to` | VARCHAR(255) | Assigned To | Links to the User or agent responsible for this record. |
| `created_by` | VARCHAR(255) | Created By | Stores the created by information. |
| `modified_by` | VARCHAR(255) | Modified By | Stores the modified by information. |
| `creation` | DATETIME | Creation | Timestamp for process scheduling or historical tracking. |
| `modified` | DATETIME | Modified | Timestamp for process scheduling or historical tracking. |
| `docstatus` | VARCHAR(255) | Docstatus | Tracks the current lifecycle status of this record. |
| `company` | VARCHAR(255) | Company | Stores the company information. |
| `territory` | VARCHAR(255) | Territory | Stores the territory information. |
| `team` | VARCHAR(255) | Team | Stores the team information. |

---

## Table: tabquotation (quotation)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `customer` | VARCHAR(255) | Customer | Stores the customer information. |
| `valid_till` | DATE | Valid Till | Stores the valid till information. |
| `status` | VARCHAR(255) | Status | Tracks the current lifecycle status of this record. |
| `total_amount` | DECIMAL(21, 9) | Total Amount | Financial value or monetary amount associated with this entry. |
| `owner` | VARCHAR(255) | Owner | Links to the User or agent responsible for this record. |
| `assigned_to` | VARCHAR(255) | Assigned To | Links to the User or agent responsible for this record. |
| `created_by` | VARCHAR(255) | Created By | Stores the created by information. |
| `modified_by` | VARCHAR(255) | Modified By | Stores the modified by information. |
| `creation` | DATETIME | Creation | Timestamp for process scheduling or historical tracking. |
| `modified` | DATETIME | Modified | Timestamp for process scheduling or historical tracking. |
| `docstatus` | VARCHAR(255) | Docstatus | Tracks the current lifecycle status of this record. |
| `company` | VARCHAR(255) | Company | Stores the company information. |
| `territory` | VARCHAR(255) | Territory | Stores the territory information. |
| `team` | VARCHAR(255) | Team | Stores the team information. |

---

## Table: tabtask (task)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `task_name` | VARCHAR(255) | Task Name | Stores the name or identifier of the task name. |
| `related_lead` | VARCHAR(255) | Lead | Stores the lead information. |
| `assignee` | VARCHAR(255) | Assignee | Stores the assignee information. |
| `due_date` | DATE | Due Date | Timestamp for process scheduling or historical tracking. |
| `status` | VARCHAR(255) | Status | Tracks the current lifecycle status of this record. |
| `priority` | VARCHAR(255) | Priority | Stores the priority information. |
| `owner` | VARCHAR(255) | Owner | Links to the User or agent responsible for this record. |
| `assigned_to` | VARCHAR(255) | Assigned To | Links to the User or agent responsible for this record. |
| `created_by` | VARCHAR(255) | Created By | Stores the created by information. |
| `modified_by` | VARCHAR(255) | Modified By | Stores the modified by information. |
| `creation` | DATETIME | Creation | Timestamp for process scheduling or historical tracking. |
| `modified` | DATETIME | Modified | Timestamp for process scheduling or historical tracking. |
| `docstatus` | VARCHAR(255) | Docstatus | Tracks the current lifecycle status of this record. |
| `company` | VARCHAR(255) | Company | Stores the company information. |
| `territory` | VARCHAR(255) | Territory | Stores the territory information. |
| `team` | VARCHAR(255) | Team | Stores the team information. |

---

## Table: tabteam (team)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `team_name` | VARCHAR(255) | Team Name | Stores the name or identifier of the team name. |
| `leader` | VARCHAR(255) | Leader | Stores the leader information. |
| `owner` | VARCHAR(255) | Owner | Links to the User or agent responsible for this record. |
| `assigned_to` | VARCHAR(255) | Assigned To | Links to the User or agent responsible for this record. |
| `created_by` | VARCHAR(255) | Created By | Stores the created by information. |
| `modified_by` | VARCHAR(255) | Modified By | Stores the modified by information. |
| `creation` | DATETIME | Creation | Timestamp for process scheduling or historical tracking. |
| `modified` | DATETIME | Modified | Timestamp for process scheduling or historical tracking. |
| `docstatus` | VARCHAR(255) | Docstatus | Tracks the current lifecycle status of this record. |
| `company` | VARCHAR(255) | Company | Stores the company information. |

---

## Table: tabterritory (territory)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `territory_name` | VARCHAR(255) | Territory Name | Stores the name or identifier of the territory name. |
| `owner` | VARCHAR(255) | Owner | Links to the User or agent responsible for this record. |
| `assigned_to` | VARCHAR(255) | Assigned To | Links to the User or agent responsible for this record. |
| `created_by` | VARCHAR(255) | Created By | Stores the created by information. |
| `modified_by` | VARCHAR(255) | Modified By | Stores the modified by information. |
| `creation` | DATETIME | Creation | Timestamp for process scheduling or historical tracking. |
| `modified` | DATETIME | Modified | Timestamp for process scheduling or historical tracking. |
| `docstatus` | VARCHAR(255) | Docstatus | Tracks the current lifecycle status of this record. |
| `company` | VARCHAR(255) | Company | Stores the company information. |

---

## Table: tabwebhook_log (webhook_log)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `webhook_url` | VARCHAR(255) | Webhook URL | Stores the webhook url information. |
| `payload` | TEXT | Payload | Stores the payload information. |
| `response` | TEXT | Response | Stores the response information. |
| `status` | VARCHAR(255) | Status | Tracks the current lifecycle status of this record. |
| `owner` | VARCHAR(255) | Owner | Links to the User or agent responsible for this record. |
| `assigned_to` | VARCHAR(255) | Assigned To | Links to the User or agent responsible for this record. |
| `created_by` | VARCHAR(255) | Created By | Stores the created by information. |
| `modified_by` | VARCHAR(255) | Modified By | Stores the modified by information. |
| `creation` | DATETIME | Creation | Timestamp for process scheduling or historical tracking. |
| `modified` | DATETIME | Modified | Timestamp for process scheduling or historical tracking. |
| `docstatus` | VARCHAR(255) | Docstatus | Tracks the current lifecycle status of this record. |

---

## Table: tabwhatsapp_conversation (whatsapp_conversation)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `phone_number` | VARCHAR(255) | Phone Number | Phone or mobile contact number. |
| `lead` | VARCHAR(255) | Lead | Stores the lead information. |
| `status` | VARCHAR(255) | Status | Tracks the current lifecycle status of this record. |
| `owner` | VARCHAR(255) | Owner | Links to the User or agent responsible for this record. |
| `assigned_to` | VARCHAR(255) | Assigned To | Links to the User or agent responsible for this record. |
| `created_by` | VARCHAR(255) | Created By | Stores the created by information. |
| `modified_by` | VARCHAR(255) | Modified By | Stores the modified by information. |
| `creation` | DATETIME | Creation | Timestamp for process scheduling or historical tracking. |
| `modified` | DATETIME | Modified | Timestamp for process scheduling or historical tracking. |
| `docstatus` | VARCHAR(255) | Docstatus | Tracks the current lifecycle status of this record. |
| `company` | VARCHAR(255) | Company | Stores the company information. |
| `territory` | VARCHAR(255) | Territory | Stores the territory information. |
| `team` | VARCHAR(255) | Team | Stores the team information. |

---

## Table: tabwhatsapp_message (whatsapp_message)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `conversation` | VARCHAR(255) | Conversation | Stores the conversation information. |
| `direction` | VARCHAR(255) | Direction | Stores the direction information. |
| `message_type` | VARCHAR(255) | Message Type | Stores the message type information. |
| `content` | TEXT | Content | Stores the content information. |
| `timestamp` | DATETIME | Timestamp | Timestamp for process scheduling or historical tracking. |
| `message_id` | VARCHAR(255) | Message ID | Stores the message id information. |
| `owner` | VARCHAR(255) | Owner | Links to the User or agent responsible for this record. |
| `assigned_to` | VARCHAR(255) | Assigned To | Links to the User or agent responsible for this record. |
| `created_by` | VARCHAR(255) | Created By | Stores the created by information. |
| `modified_by` | VARCHAR(255) | Modified By | Stores the modified by information. |
| `creation` | DATETIME | Creation | Timestamp for process scheduling or historical tracking. |
| `modified` | DATETIME | Modified | Timestamp for process scheduling or historical tracking. |
| `docstatus` | VARCHAR(255) | Docstatus | Tracks the current lifecycle status of this record. |
| `company` | VARCHAR(255) | Company | Stores the company information. |
| `territory` | VARCHAR(255) | Territory | Stores the territory information. |
| `team` | VARCHAR(255) | Team | Stores the team information. |

---

## Table: tabworkflow_action (workflow_action)

| Field Name | SQL Type | Label | Business Purpose |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Name | Primary key identifier for the record |
| `action_name` | VARCHAR(255) | Action Name | Stores the name or identifier of the action name. |
| `workflow_name` | VARCHAR(255) | Workflow Name | Stores the name or identifier of the workflow name. |
| `allowed_role` | VARCHAR(255) | Allowed Role | Stores the allowed role information. |
| `owner` | VARCHAR(255) | Owner | Links to the User or agent responsible for this record. |
| `assigned_to` | VARCHAR(255) | Assigned To | Links to the User or agent responsible for this record. |
| `created_by` | VARCHAR(255) | Created By | Stores the created by information. |
| `modified_by` | VARCHAR(255) | Modified By | Stores the modified by information. |
| `creation` | DATETIME | Creation | Timestamp for process scheduling or historical tracking. |
| `modified` | DATETIME | Modified | Timestamp for process scheduling or historical tracking. |
| `docstatus` | VARCHAR(255) | Docstatus | Tracks the current lifecycle status of this record. |

---

