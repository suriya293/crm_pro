# CRM Pro Table Structure Specifications

## tabCRM Activity (CRM Activity)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `activity_type` | VARCHAR(255) | Yes | Call, Meeting, Task, Email, WhatsApp | None | Activity Type |
| `lead` | VARCHAR(255) | No | CRM Lead | None | Associated Lead |
| `deal` | VARCHAR(255) | No | CRM Deal | None | Associated Deal |
| `notes` | TEXT | No | None | None | Notes |
| `activity_date` | DATETIME | No | None | None | Activity Date |

---

## tabCRM Attachment (CRM Attachment)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `lead` | VARCHAR(255) | No | CRM Lead | None | Associated Lead |
| `deal` | VARCHAR(255) | No | CRM Deal | None | Associated Deal |
| `file_url` | VARCHAR(255) | Yes | None | None | File Attachment |
| `file_name` | VARCHAR(255) | No | None | None | File Name |

---

## tabCRM Audit Log (CRM Audit Log)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `ref_doctype` | VARCHAR(255) | Yes | None | None | Referenced DocType |
| `ref_name` | VARCHAR(255) | Yes | None | None | Referenced ID |
| `action` | VARCHAR(255) | Yes | Create, Update, Delete | None | Action Taken |
| `user` | VARCHAR(255) | Yes | User | None | User |
| `details` | TEXT | No | None | None | Audit Details |

---

## tabCRM Call Log (CRM Call Log)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `lead` | VARCHAR(255) | No | CRM Lead | None | Associated Lead |
| `phone_number` | VARCHAR(255) | No | None | None | Phone Number |
| `duration_seconds` | INT(11) | No | None | None | Duration (Seconds) |
| `call_type` | VARCHAR(255) | No | Inbound, Outbound, Missed | None | Call Type |
| `recording_url` | VARCHAR(255) | No | None | None | Recording URL |
| `summary` | TEXT | No | None | None | Summary |

---

## tabCRM Company (CRM Company)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `company_name` | VARCHAR(255) | Yes | None | None | Company Name |
| `website` | VARCHAR(255) | No | None | None | Website |
| `industry` | VARCHAR(255) | No | None | None | Industry |
| `employee_count` | INT(11) | No | None | None | Employee Count |
| `annual_revenue` | DECIMAL(21, 9) | No | None | None | Annual Revenue |
| `address` | TEXT | No | None | None | Address |

---

## tabCRM Contact (CRM Contact)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `contact_name` | VARCHAR(255) | Yes | None | None | Contact Name |
| `company` | VARCHAR(255) | No | CRM Company | None | Company |
| `lead` | VARCHAR(255) | No | CRM Lead | None | Associated Lead |
| `job_title` | VARCHAR(255) | No | None | None | Job Title |
| `history_summary` | TEXT | No | None | None | Contact History Summary |

---

## tabCRM Contact Email (CRM Contact Email)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `email` | VARCHAR(255) | Yes | None | None | Email Address |
| `type` | VARCHAR(255) | No | Work, Personal | None | Type |

---

## tabCRM Contact Phone (CRM Contact Phone)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `phone` | VARCHAR(255) | Yes | None | None | Phone Number |
| `type` | VARCHAR(255) | No | Mobile, Work, Home | None | Type |

---

## tabCRM Custom Field (CRM Custom Field)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `field_name` | VARCHAR(255) | Yes | None | None | Field Name |
| `field_value` | VARCHAR(255) | Yes | None | None | Field Value |

---

## tabCRM Dashboard Metrics (CRM Dashboard Metrics)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `metric_date` | DATE | Yes | None | None | Metric Date |
| `total_leads` | INT(11) | No | None | None | Total Leads |
| `new_leads` | INT(11) | No | None | None | New Leads |
| `converted_leads` | INT(11) | No | None | None | Converted Leads |
| `won_deals` | INT(11) | No | None | None | Won Deals |
| `lost_deals` | INT(11) | No | None | None | Lost Deals |
| `total_revenue` | DECIMAL(21, 9) | No | None | None | Total Revenue |

---

## tabCRM Deal (CRM Deal)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `deal_name` | VARCHAR(255) | Yes | None | None | Deal Name |
| `lead` | VARCHAR(255) | No | CRM Lead | None | Lead Source |
| `company` | VARCHAR(255) | No | CRM Company | None | Company |
| `deal_stage` | VARCHAR(255) | No | CRM Pipeline Stage | None | Deal Stage |
| `deal_value` | DECIMAL(21, 9) | Yes | None | None | Deal Value |
| `expected_close` | DATE | No | None | None | Expected Close Date |
| `forecast_category` | VARCHAR(255) | No | Pipeline, Best Case, Commit, Closed | None | Forecast Category |
| `deal_status` | VARCHAR(255) | No | Open, Won, Lost | None | Deal Status |

---

## tabCRM Email Log (CRM Email Log)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `lead` | VARCHAR(255) | No | CRM Lead | None | Associated Lead |
| `sender` | VARCHAR(255) | No | None | None | Sender |
| `recipient` | VARCHAR(255) | No | None | None | Recipient |
| `subject` | VARCHAR(255) | No | None | None | Subject |
| `body` | TEXT | No | None | None | Body Content |
| `sent_received` | VARCHAR(255) | No | Sent, Received | None | Direction |

---

## tabCRM Lead (CRM Lead)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `lead_name` | VARCHAR(255) | Yes | None | None | Lead Name |
| `email` | VARCHAR(255) | No | None | None | Email |
| `mobile` | VARCHAR(255) | No | None | None | Mobile |
| `country_code` | VARCHAR(255) | No | None | None | Country Code |
| `stage` | VARCHAR(255) | No | CRM Pipeline Stage | None | Stage |
| `source` | VARCHAR(255) | No | None | None | Source |
| `user` | VARCHAR(255) | No | User | None | User |
| `priority` | VARCHAR(255) | No | Low, Medium, High | None | Priority |
| `segment` | VARCHAR(255) | No | Enterprise, Mid-Market, SMB | None | Segment |
| `alt_mobile_1` | VARCHAR(255) | No | None | None | Alternate Mobile 1 |
| `alt_mobile_2` | VARCHAR(255) | No | None | None | Alternate Mobile 2 |
| `alt_mobile_3` | VARCHAR(255) | No | None | None | Alternate Mobile 3 |
| `age` | INT(11) | No | None | None | Age |
| `gender` | VARCHAR(255) | No | Male, Female, Other | None | Gender |
| `address` | TEXT | No | None | None | Address |
| `state` | VARCHAR(255) | No | None | None | State |
| `city` | VARCHAR(255) | No | None | None | City |
| `country` | VARCHAR(255) | No | None | None | Country |
| `pincode` | VARCHAR(255) | No | None | None | Pincode |
| `company_name` | VARCHAR(255) | No | None | None | Company Name |
| `designation` | VARCHAR(255) | No | None | None | Designation |
| `website` | VARCHAR(255) | No | None | None | Website |
| `tags` | VARCHAR(255) | No | None | None | Tags |
| `opportunity_value` | DECIMAL(21, 9) | No | None | None | Opportunity Value |
| `followup_date` | DATETIME | No | None | None | Follow-up Date |

---

## tabCRM Lead Snapshot (CRM Lead Snapshot)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `snapshot_date` | DATE | Yes | None | None | Snapshot Date |
| `total_leads` | INT(11) | No | None | 0 | Total Leads |
| `active_leads` | INT(11) | No | None | 0 | Active Leads |
| `converted_leads` | INT(11) | No | None | 0 | Converted Leads |
| `conversion_rate` | DECIMAL(21, 9) | No | None | 0.0 | Conversion Rate |

---

## tabCRM Meeting (CRM Meeting)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `meeting_subject` | VARCHAR(255) | Yes | None | None | Meeting Subject |
| `lead` | VARCHAR(255) | No | CRM Lead | None | Associated Lead |
| `meeting_time` | DATETIME | Yes | None | None | Meeting Time |
| `location` | VARCHAR(255) | No | None | None | Location |
| `agenda` | TEXT | No | None | None | Agenda |

---

## tabCRM Note (CRM Note)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `lead` | VARCHAR(255) | No | CRM Lead | None | Associated Lead |
| `deal` | VARCHAR(255) | No | CRM Deal | None | Associated Deal |
| `content` | TEXT | Yes | None | None | Note Content |
| `added_by` | VARCHAR(255) | No | User | None | Added By |

---

## tabCRM Notification (CRM Notification)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `notification_title` | VARCHAR(255) | Yes | None | None | Notification Title |
| `message` | TEXT | Yes | None | None | Message Content |
| `for_user` | VARCHAR(255) | Yes | User | None | For User |
| `is_read` | INT(11) | No | None | None | Is Read |

---

## tabCRM Pipeline (CRM Pipeline)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `pipeline_name` | VARCHAR(255) | Yes | None | None | Pipeline Name |
| `description` | TEXT | No | None | None | Description |

---

## tabCRM Pipeline Stage (CRM Pipeline Stage)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `stage_name` | VARCHAR(255) | Yes | None | None | Stage Name |
| `pipeline` | VARCHAR(255) | Yes | CRM Pipeline | None | Pipeline |
| `order` | INT(11) | No | None | None | Order |
| `color` | VARCHAR(255) | No | None | None | Color Hex |

---

## tabCRM Reminder (CRM Reminder)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `reminder_subject` | VARCHAR(255) | Yes | None | None | Reminder Subject |
| `lead` | VARCHAR(255) | No | CRM Lead | None | Associated Lead |
| `reminder_time` | DATETIME | Yes | None | None | Reminder Time |
| `is_sent` | INT(11) | No | None | None | Is Sent |
| `recipient` | VARCHAR(255) | No | User | None | Recipient |

---

## tabCRM Role Configuration (CRM Role Configuration)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `role_name` | VARCHAR(255) | Yes | None | None | Role Name |
| `allowed_views` | TEXT | No | None | None | Allowed Views |
| `allowed_actions` | TEXT | No | None | None | Allowed Actions |

---

## tabCRM Sales Target (CRM Sales Target)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `target_name` | VARCHAR(255) | Yes | None | None | Target Name |
| `target_type` | VARCHAR(255) | Yes | User, Team | None | Target Type |
| `user` | VARCHAR(255) | No | User | None | User |
| `team` | VARCHAR(255) | No | CRM Team | None | Team |
| `target_value` | DECIMAL(21, 9) | Yes | None | None | Target Value |
| `achieved_value` | DECIMAL(21, 9) | No | None | None | Achieved Value |
| `fiscal_year` | VARCHAR(255) | No | None | None | Fiscal Year |

---

## tabCRM Settings (CRM Settings)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `company_name` | VARCHAR(255) | No | None | Precision CRM | Company Name |
| `default_pipeline` | VARCHAR(255) | No | CRM Pipeline | None | Default Pipeline |
| `enable_ai_suggestions` | INT(11) | No | None | 1 | Enable AI Suggestions |
| `enable_whatsapp_integration` | INT(11) | No | None | None | Enable WhatsApp Integration |
| `whatsapp_access_token` | VARCHAR(255) | No | None | None | WhatsApp Access Token |
| `whatsapp_phone_number_id` | VARCHAR(255) | No | None | None | WhatsApp Phone Number ID |
| `facebook_access_token` | VARCHAR(255) | No | None | None | Facebook Access Token |
| `facebook_webhook_verify_token` | VARCHAR(255) | No | None | None | Facebook Webhook Verify Token |
| `facebook_app_secret` | VARCHAR(255) | No | None | None | Facebook App Secret |

---

## tabCRM Task (CRM Task)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `task_subject` | VARCHAR(255) | Yes | None | None | Task Subject |
| `lead` | VARCHAR(255) | No | CRM Lead | None | Associated Lead |
| `deal` | VARCHAR(255) | No | CRM Deal | None | Associated Deal |
| `due_date` | DATE | No | None | None | Due Date |
| `status` | VARCHAR(255) | No | Open, In Progress, Completed, Cancelled | None | Status |
| `assigned_to` | VARCHAR(255) | No | User | None | Assigned To |

---

## tabCRM Team (CRM Team)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `team_name` | VARCHAR(255) | Yes | None | None | Team Name |
| `lead_user` | VARCHAR(255) | No | User | None | Team Lead |
| `description` | TEXT | No | None | None | Description |

---

## tabCRM User Profile (CRM User Profile)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `user` | VARCHAR(255) | Yes | User | None | User Link |
| `phone_number` | VARCHAR(255) | No | None | None | Phone Number |
| `profile_picture` | VARCHAR(255) | No | None | None | Profile Picture |
| `designation` | VARCHAR(255) | No | None | None | Designation |
| `team` | VARCHAR(255) | No | CRM Team | None | Associated Team |

---

## tabCRM WhatsApp Log (CRM WhatsApp Log)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `lead` | VARCHAR(255) | No | CRM Lead | None | Associated Lead |
| `phone_number` | VARCHAR(255) | No | None | None | Phone Number |
| `message` | TEXT | No | None | None | Message Content |
| `direction` | VARCHAR(255) | No | Outbound, Inbound | None | Direction |

---

## tabactivity (activity)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `activity_type` | VARCHAR(255) | Yes | Call, Email, Meeting, Task, Note | None | Activity Type |
| `lead` | VARCHAR(255) | No | Lead | None | Lead |
| `description` | TEXT | No | None | None | Description |
| `timestamp` | DATETIME | No | None | Now | Timestamp |
| `performed_by` | VARCHAR(255) | No | User | None | Performed By |
| `owner` | VARCHAR(255) | No | User | None | Owner |
| `assigned_to` | VARCHAR(255) | No | User | None | Assigned To |
| `created_by` | VARCHAR(255) | No | User | None | Created By |
| `modified_by` | VARCHAR(255) | No | User | None | Modified By |
| `creation` | DATETIME | No | None | None | Creation |
| `modified` | DATETIME | No | None | None | Modified |
| `docstatus` | VARCHAR(255) | No | 0, 1, 2 | None | Docstatus |
| `company` | VARCHAR(255) | No | Company | None | Company |
| `territory` | VARCHAR(255) | No | Territory | None | Territory |
| `team` | VARCHAR(255) | No | Team | None | Team |

---

## tabapi_log (api_log)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `endpoint` | VARCHAR(255) | Yes | None | None | Endpoint |
| `method` | VARCHAR(255) | Yes | None | None | Method |
| `ip_address` | VARCHAR(255) | No | None | None | IP Address |
| `user` | VARCHAR(255) | No | User | None | User |
| `status` | VARCHAR(255) | No | Success, Failed | Success | Status |
| `owner` | VARCHAR(255) | No | User | None | Owner |
| `assigned_to` | VARCHAR(255) | No | User | None | Assigned To |
| `created_by` | VARCHAR(255) | No | User | None | Created By |
| `modified_by` | VARCHAR(255) | No | User | None | Modified By |
| `creation` | DATETIME | No | None | None | Creation |
| `modified` | DATETIME | No | None | None | Modified |
| `docstatus` | VARCHAR(255) | No | 0, 1, 2 | None | Docstatus |

---

## tabaudit_log (audit_log)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `action` | VARCHAR(255) | Yes | None | None | Action |
| `details` | TEXT | No | None | None | Details |
| `user` | VARCHAR(255) | No | User | None | User |
| `timestamp` | DATETIME | No | None | Now | Timestamp |
| `owner` | VARCHAR(255) | No | User | None | Owner |
| `assigned_to` | VARCHAR(255) | No | User | None | Assigned To |
| `created_by` | VARCHAR(255) | No | User | None | Created By |
| `modified_by` | VARCHAR(255) | No | User | None | Modified By |
| `creation` | DATETIME | No | None | None | Creation |
| `modified` | DATETIME | No | None | None | Modified |
| `docstatus` | VARCHAR(255) | No | 0, 1, 2 | None | Docstatus |

---

## tabautomation_rule (automation_rule)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `rule_name` | VARCHAR(255) | Yes | None | None | Rule Name |
| `trigger_event` | VARCHAR(255) | Yes | On Insert, On Update, On Submit, On Cancel | None | Trigger Event |
| `target_doctype` | VARCHAR(255) | Yes | None | None | Target DocType |
| `action` | TEXT | Yes | None | None | Action |
| `is_active` | INT(11) | No | None | 1 | Is Active |
| `owner` | VARCHAR(255) | No | User | None | Owner |
| `assigned_to` | VARCHAR(255) | No | User | None | Assigned To |
| `created_by` | VARCHAR(255) | No | User | None | Created By |
| `modified_by` | VARCHAR(255) | No | User | None | Modified By |
| `creation` | DATETIME | No | None | None | Creation |
| `modified` | DATETIME | No | None | None | Modified |
| `docstatus` | VARCHAR(255) | No | 0, 1, 2 | None | Docstatus |

---

## tabcampaign (campaign)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `campaign_name` | VARCHAR(255) | Yes | None | None | Campaign Name |
| `start_date` | DATE | Yes | None | None | Start Date |
| `end_date` | DATE | No | None | None | End Date |
| `budget` | DECIMAL(21, 9) | No | None | None | Budget |
| `target_audience` | VARCHAR(255) | No | None | None | Target Audience |
| `status` | VARCHAR(255) | No | Draft, Active, Completed, Cancelled | Draft | Status |
| `owner` | VARCHAR(255) | No | User | None | Owner |
| `assigned_to` | VARCHAR(255) | No | User | None | Assigned To |
| `created_by` | VARCHAR(255) | No | User | None | Created By |
| `modified_by` | VARCHAR(255) | No | User | None | Modified By |
| `creation` | DATETIME | No | None | None | Creation |
| `modified` | DATETIME | No | None | None | Modified |
| `docstatus` | VARCHAR(255) | No | 0, 1, 2 | None | Docstatus |
| `company` | VARCHAR(255) | No | Company | None | Company |
| `territory` | VARCHAR(255) | No | Territory | None | Territory |
| `team` | VARCHAR(255) | No | Team | None | Team |

---

## tabcompany (company)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `company_name` | VARCHAR(255) | Yes | None | None | Company Name |
| `address` | TEXT | No | None | None | Address |
| `industry` | VARCHAR(255) | No | None | None | Industry |
| `website` | VARCHAR(255) | No | None | None | Website |
| `account_manager` | VARCHAR(255) | No | User | None | Account Manager |
| `owner` | VARCHAR(255) | No | User | None | Owner |
| `assigned_to` | VARCHAR(255) | No | User | None | Assigned To |
| `created_by` | VARCHAR(255) | No | User | None | Created By |
| `modified_by` | VARCHAR(255) | No | User | None | Modified By |
| `creation` | DATETIME | No | None | None | Creation |
| `modified` | DATETIME | No | None | None | Modified |
| `docstatus` | VARCHAR(255) | No | 0, 1, 2 | None | Docstatus |
| `company` | VARCHAR(255) | No | Company | None | Company |
| `territory` | VARCHAR(255) | No | Territory | None | Territory |
| `team` | VARCHAR(255) | No | Team | None | Team |

---

## tabcontact (contact)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `contact_name` | VARCHAR(255) | Yes | None | None | Contact Name |
| `first_name` | VARCHAR(255) | No | None | None | First Name |
| `last_name` | VARCHAR(255) | No | None | None | Last Name |
| `email` | VARCHAR(255) | No | None | None | Email |
| `mobile_no` | VARCHAR(255) | No | None | None | Mobile Number |
| `associated_lead` | VARCHAR(255) | No | Lead | None | Lead |
| `company` | VARCHAR(255) | No | Company | None | Company |
| `role` | VARCHAR(255) | No | None | None | Role |
| `created_at` | DATETIME | No | None | Now | Created At |
| `updated_at` | DATETIME | No | None | Now | Updated At |

---

## tabdeal (deal)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `deal_name` | VARCHAR(255) | Yes | None | None | Deal Name |
| `opportunity` | VARCHAR(255) | Yes | Opportunity | None | Opportunity |
| `amount` | DECIMAL(21, 9) | No | None | None | Amount |
| `stage` | VARCHAR(255) | No | Prospect, Negotiation, Won, Lost | Prospect | Stage |
| `expected_close_date` | DATE | No | None | None | Expected Close Date |
| `owner` | VARCHAR(255) | No | User | None | Owner |
| `assigned_to` | VARCHAR(255) | No | User | None | Assigned To |
| `created_by` | VARCHAR(255) | No | User | None | Created By |
| `modified_by` | VARCHAR(255) | No | User | None | Modified By |
| `creation` | DATETIME | No | None | None | Creation |
| `modified` | DATETIME | No | None | None | Modified |
| `docstatus` | VARCHAR(255) | No | 0, 1, 2 | None | Docstatus |
| `company` | VARCHAR(255) | No | Company | None | Company |
| `territory` | VARCHAR(255) | No | Territory | None | Territory |
| `team` | VARCHAR(255) | No | Team | None | Team |

---

## tabdepartment (department)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `department_name` | VARCHAR(255) | Yes | None | None | Department Name |
| `owner` | VARCHAR(255) | No | User | None | Owner |
| `assigned_to` | VARCHAR(255) | No | User | None | Assigned To |
| `created_by` | VARCHAR(255) | No | User | None | Created By |
| `modified_by` | VARCHAR(255) | No | User | None | Modified By |
| `creation` | DATETIME | No | None | None | Creation |
| `modified` | DATETIME | No | None | None | Modified |
| `docstatus` | VARCHAR(255) | No | 0, 1, 2 | None | Docstatus |
| `company` | VARCHAR(255) | No | Company | None | Company |

---

## tabexport_job (export_job)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `doctype_to_export` | VARCHAR(255) | Yes | None | None | DocType to Export |
| `file_path` | VARCHAR(255) | No | None | None | File Path |
| `status` | VARCHAR(255) | No | Pending, Processing, Completed, Failed | Pending | Status |
| `owner` | VARCHAR(255) | No | User | None | Owner |
| `assigned_to` | VARCHAR(255) | No | User | None | Assigned To |
| `created_by` | VARCHAR(255) | No | User | None | Created By |
| `modified_by` | VARCHAR(255) | No | User | None | Modified By |
| `creation` | DATETIME | No | None | None | Creation |
| `modified` | DATETIME | No | None | None | Modified |
| `docstatus` | VARCHAR(255) | No | 0, 1, 2 | None | Docstatus |

---

## tabfacebook_lead (facebook_lead)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `facebook_lead_id` | VARCHAR(255) | Yes | None | None | Facebook Lead ID |
| `form_name` | VARCHAR(255) | Yes | None | None | Form Name |
| `campaign` | VARCHAR(255) | No | Campaign | None | Campaign |
| `lead_info` | TEXT | No | None | None | Lead Info |
| `sync_status` | VARCHAR(255) | No | Pending, Synced, Failed | Pending | Sync Status |
| `owner` | VARCHAR(255) | No | User | None | Owner |
| `assigned_to` | VARCHAR(255) | No | User | None | Assigned To |
| `created_by` | VARCHAR(255) | No | User | None | Created By |
| `modified_by` | VARCHAR(255) | No | User | None | Modified By |
| `creation` | DATETIME | No | None | None | Creation |
| `modified` | DATETIME | No | None | None | Modified |
| `docstatus` | VARCHAR(255) | No | 0, 1, 2 | None | Docstatus |
| `company` | VARCHAR(255) | No | Company | None | Company |
| `territory` | VARCHAR(255) | No | Territory | None | Territory |
| `team` | VARCHAR(255) | No | Team | None | Team |

---

## tabfollowup (followup)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `followup_date` | DATE | Yes | None | None | Follow‑up Date |
| `lead` | VARCHAR(255) | Yes | Lead | None | Lead |
| `notes` | TEXT | No | None | None | Notes |
| `outcome` | VARCHAR(255) | No | Pending, Successful, Unsuccessful | None | Outcome |
| `next_step` | VARCHAR(255) | No | None | None | Next Step |
| `owner` | VARCHAR(255) | No | User | None | Owner |
| `assigned_to` | VARCHAR(255) | No | User | None | Assigned To |
| `created_by` | VARCHAR(255) | No | User | None | Created By |
| `modified_by` | VARCHAR(255) | No | User | None | Modified By |
| `creation` | DATETIME | No | None | None | Creation |
| `modified` | DATETIME | No | None | None | Modified |
| `docstatus` | VARCHAR(255) | No | 0, 1, 2 | None | Docstatus |
| `company` | VARCHAR(255) | No | Company | None | Company |
| `territory` | VARCHAR(255) | No | Territory | None | Territory |
| `team` | VARCHAR(255) | No | Team | None | Team |

---

## tabimport_job (import_job)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `file_path` | VARCHAR(255) | Yes | None | None | File Path |
| `doctype_to_import` | VARCHAR(255) | Yes | None | None | DocType to Import |
| `status` | VARCHAR(255) | No | Pending, Processing, Completed, Failed | Pending | Status |
| `owner` | VARCHAR(255) | No | User | None | Owner |
| `assigned_to` | VARCHAR(255) | No | User | None | Assigned To |
| `created_by` | VARCHAR(255) | No | User | None | Created By |
| `modified_by` | VARCHAR(255) | No | User | None | Modified By |
| `creation` | DATETIME | No | None | None | Creation |
| `modified` | DATETIME | No | None | None | Modified |
| `docstatus` | VARCHAR(255) | No | 0, 1, 2 | None | Docstatus |

---

## tabinvoice (invoice)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `customer` | VARCHAR(255) | Yes | Contact | None | Customer |
| `posting_date` | DATE | Yes | None | None | Posting Date |
| `status` | VARCHAR(255) | No | Draft, Unpaid, Paid, Overdue, Cancelled | Draft | Status |
| `grand_total` | DECIMAL(21, 9) | No | None | None | Grand Total |
| `owner` | VARCHAR(255) | No | User | None | Owner |
| `assigned_to` | VARCHAR(255) | No | User | None | Assigned To |
| `created_by` | VARCHAR(255) | No | User | None | Created By |
| `modified_by` | VARCHAR(255) | No | User | None | Modified By |
| `creation` | DATETIME | No | None | None | Creation |
| `modified` | DATETIME | No | None | None | Modified |
| `docstatus` | VARCHAR(255) | No | 0, 1, 2 | None | Docstatus |
| `company` | VARCHAR(255) | No | Company | None | Company |
| `territory` | VARCHAR(255) | No | Territory | None | Territory |
| `team` | VARCHAR(255) | No | Team | None | Team |

---

## tablead (lead)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `lead_name` | VARCHAR(255) | Yes | None | None | Lead Name |
| `lead_source` | VARCHAR(255) | No | Website, Referral, Advertisement, Other | None | Lead Source |
| `mobile_no` | VARCHAR(255) | Yes | None | None | Mobile Number |
| `email` | VARCHAR(255) | No | None | None | Email |
| `status` | VARCHAR(255) | No | New, Assigned, Attempted Contact, Contacted, Interested, Qualified, Converted, Lost, Duplicate | New | Status |
| `assigned_to` | VARCHAR(255) | No | User | None | Assigned To |
| `created_at` | DATETIME | No | None | Now | Created At |
| `updated_at` | DATETIME | No | None | Now | Updated At |

---

## tablead_source (lead_source)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `source_name` | VARCHAR(255) | Yes | None | None | Source Name |
| `owner` | VARCHAR(255) | No | User | None | Owner |
| `assigned_to` | VARCHAR(255) | No | User | None | Assigned To |
| `created_by` | VARCHAR(255) | No | User | None | Created By |
| `modified_by` | VARCHAR(255) | No | User | None | Modified By |
| `creation` | DATETIME | No | None | None | Creation |
| `modified` | DATETIME | No | None | None | Modified |
| `docstatus` | VARCHAR(255) | No | 0, 1, 2 | None | Docstatus |
| `company` | VARCHAR(255) | No | Company | None | Company |
| `territory` | VARCHAR(255) | No | Territory | None | Territory |
| `team` | VARCHAR(255) | No | Team | None | Team |

---

## tabnotification (notification)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `subject` | VARCHAR(255) | Yes | None | None | Subject |
| `message` | TEXT | Yes | None | None | Message |
| `for_user` | VARCHAR(255) | Yes | User | None | For User |
| `is_read` | INT(11) | No | None | None | Is Read |
| `owner` | VARCHAR(255) | No | User | None | Owner |
| `assigned_to` | VARCHAR(255) | No | User | None | Assigned To |
| `created_by` | VARCHAR(255) | No | User | None | Created By |
| `modified_by` | VARCHAR(255) | No | User | None | Modified By |
| `creation` | DATETIME | No | None | None | Creation |
| `modified` | DATETIME | No | None | None | Modified |
| `docstatus` | VARCHAR(255) | No | 0, 1, 2 | None | Docstatus |

---

## tabopportunity (opportunity)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `opportunity_name` | VARCHAR(255) | Yes | None | None | Opportunity Name |
| `lead` | VARCHAR(255) | Yes | Lead | None | Lead |
| `value` | DECIMAL(21, 9) | No | None | None | Value |
| `probability` | INT(11) | No | None | None | Probability |
| `expected_closure` | DATE | No | None | None | Expected Closure |
| `status` | VARCHAR(255) | No | Open, Discovery, Qualification, Proposal Sent, Negotiation, Won, Lost, On Hold | Open | Status |
| `owner` | VARCHAR(255) | No | User | None | Owner |
| `assigned_to` | VARCHAR(255) | No | User | None | Assigned To |
| `created_by` | VARCHAR(255) | No | User | None | Created By |
| `modified_by` | VARCHAR(255) | No | User | None | Modified By |
| `creation` | DATETIME | No | None | None | Creation |
| `modified` | DATETIME | No | None | None | Modified |
| `docstatus` | VARCHAR(255) | No | 0, 1, 2 | None | Docstatus |
| `company` | VARCHAR(255) | No | Company | None | Company |
| `territory` | VARCHAR(255) | No | Territory | None | Territory |
| `team` | VARCHAR(255) | No | Team | None | Team |

---

## tabpayment_entry (payment_entry)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `invoice` | VARCHAR(255) | Yes | Invoice | None | Invoice |
| `amount` | DECIMAL(21, 9) | Yes | None | None | Amount |
| `payment_date` | DATE | No | None | None | Payment Date |
| `status` | VARCHAR(255) | No | Draft, Confirmed, Cancelled | Draft | Status |
| `owner` | VARCHAR(255) | No | User | None | Owner |
| `assigned_to` | VARCHAR(255) | No | User | None | Assigned To |
| `created_by` | VARCHAR(255) | No | User | None | Created By |
| `modified_by` | VARCHAR(255) | No | User | None | Modified By |
| `creation` | DATETIME | No | None | None | Creation |
| `modified` | DATETIME | No | None | None | Modified |
| `docstatus` | VARCHAR(255) | No | 0, 1, 2 | None | Docstatus |
| `company` | VARCHAR(255) | No | Company | None | Company |
| `territory` | VARCHAR(255) | No | Territory | None | Territory |
| `team` | VARCHAR(255) | No | Team | None | Team |

---

## tabprice_list (price_list)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `price_list_name` | VARCHAR(255) | Yes | None | None | Price List Name |
| `product` | VARCHAR(255) | Yes | Product | None | Product |
| `price` | DECIMAL(21, 9) | Yes | None | None | Price |
| `owner` | VARCHAR(255) | No | User | None | Owner |
| `assigned_to` | VARCHAR(255) | No | User | None | Assigned To |
| `created_by` | VARCHAR(255) | No | User | None | Created By |
| `modified_by` | VARCHAR(255) | No | User | None | Modified By |
| `creation` | DATETIME | No | None | None | Creation |
| `modified` | DATETIME | No | None | None | Modified |
| `docstatus` | VARCHAR(255) | No | 0, 1, 2 | None | Docstatus |
| `company` | VARCHAR(255) | No | Company | None | Company |
| `territory` | VARCHAR(255) | No | Territory | None | Territory |
| `team` | VARCHAR(255) | No | Team | None | Team |

---

## tabproduct (product)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `product_name` | VARCHAR(255) | Yes | None | None | Product Name |
| `product_category` | VARCHAR(255) | Yes | Product Category | None | Product Category |
| `is_active` | INT(11) | No | None | 1 | Is Active |
| `description` | TEXT | No | None | None | Description |
| `owner` | VARCHAR(255) | No | User | None | Owner |
| `assigned_to` | VARCHAR(255) | No | User | None | Assigned To |
| `created_by` | VARCHAR(255) | No | User | None | Created By |
| `modified_by` | VARCHAR(255) | No | User | None | Modified By |
| `creation` | DATETIME | No | None | None | Creation |
| `modified` | DATETIME | No | None | None | Modified |
| `docstatus` | VARCHAR(255) | No | 0, 1, 2 | None | Docstatus |
| `company` | VARCHAR(255) | No | Company | None | Company |
| `territory` | VARCHAR(255) | No | Territory | None | Territory |
| `team` | VARCHAR(255) | No | Team | None | Team |

---

## tabproduct_category (product_category)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `category_name` | VARCHAR(255) | Yes | None | None | Category Name |
| `owner` | VARCHAR(255) | No | User | None | Owner |
| `assigned_to` | VARCHAR(255) | No | User | None | Assigned To |
| `created_by` | VARCHAR(255) | No | User | None | Created By |
| `modified_by` | VARCHAR(255) | No | User | None | Modified By |
| `creation` | DATETIME | No | None | None | Creation |
| `modified` | DATETIME | No | None | None | Modified |
| `docstatus` | VARCHAR(255) | No | 0, 1, 2 | None | Docstatus |
| `company` | VARCHAR(255) | No | Company | None | Company |
| `territory` | VARCHAR(255) | No | Territory | None | Territory |
| `team` | VARCHAR(255) | No | Team | None | Team |

---

## tabquotation (quotation)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `customer` | VARCHAR(255) | Yes | Contact | None | Customer |
| `valid_till` | DATE | Yes | None | None | Valid Till |
| `status` | VARCHAR(255) | No | Draft, Sent, Accepted, Rejected | Draft | Status |
| `total_amount` | DECIMAL(21, 9) | No | None | None | Total Amount |
| `owner` | VARCHAR(255) | No | User | None | Owner |
| `assigned_to` | VARCHAR(255) | No | User | None | Assigned To |
| `created_by` | VARCHAR(255) | No | User | None | Created By |
| `modified_by` | VARCHAR(255) | No | User | None | Modified By |
| `creation` | DATETIME | No | None | None | Creation |
| `modified` | DATETIME | No | None | None | Modified |
| `docstatus` | VARCHAR(255) | No | 0, 1, 2 | None | Docstatus |
| `company` | VARCHAR(255) | No | Company | None | Company |
| `territory` | VARCHAR(255) | No | Territory | None | Territory |
| `team` | VARCHAR(255) | No | Team | None | Team |

---

## tabtask (task)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `task_name` | VARCHAR(255) | Yes | None | None | Task Name |
| `related_lead` | VARCHAR(255) | No | Lead | None | Lead |
| `assignee` | VARCHAR(255) | No | User | None | Assignee |
| `due_date` | DATE | No | None | None | Due Date |
| `status` | VARCHAR(255) | No | Open, In Progress, Completed, Cancelled | Open | Status |
| `priority` | VARCHAR(255) | No | Low, Medium, High | Medium | Priority |
| `owner` | VARCHAR(255) | No | User | None | Owner |
| `assigned_to` | VARCHAR(255) | No | User | None | Assigned To |
| `created_by` | VARCHAR(255) | No | User | None | Created By |
| `modified_by` | VARCHAR(255) | No | User | None | Modified By |
| `creation` | DATETIME | No | None | None | Creation |
| `modified` | DATETIME | No | None | None | Modified |
| `docstatus` | VARCHAR(255) | No | 0, 1, 2 | None | Docstatus |
| `company` | VARCHAR(255) | No | Company | None | Company |
| `territory` | VARCHAR(255) | No | Territory | None | Territory |
| `team` | VARCHAR(255) | No | Team | None | Team |

---

## tabteam (team)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `team_name` | VARCHAR(255) | Yes | None | None | Team Name |
| `leader` | VARCHAR(255) | No | User | None | Leader |
| `owner` | VARCHAR(255) | No | User | None | Owner |
| `assigned_to` | VARCHAR(255) | No | User | None | Assigned To |
| `created_by` | VARCHAR(255) | No | User | None | Created By |
| `modified_by` | VARCHAR(255) | No | User | None | Modified By |
| `creation` | DATETIME | No | None | None | Creation |
| `modified` | DATETIME | No | None | None | Modified |
| `docstatus` | VARCHAR(255) | No | 0, 1, 2 | None | Docstatus |
| `company` | VARCHAR(255) | No | Company | None | Company |

---

## tabterritory (territory)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `territory_name` | VARCHAR(255) | Yes | None | None | Territory Name |
| `owner` | VARCHAR(255) | No | User | None | Owner |
| `assigned_to` | VARCHAR(255) | No | User | None | Assigned To |
| `created_by` | VARCHAR(255) | No | User | None | Created By |
| `modified_by` | VARCHAR(255) | No | User | None | Modified By |
| `creation` | DATETIME | No | None | None | Creation |
| `modified` | DATETIME | No | None | None | Modified |
| `docstatus` | VARCHAR(255) | No | 0, 1, 2 | None | Docstatus |
| `company` | VARCHAR(255) | No | Company | None | Company |

---

## tabwebhook_log (webhook_log)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `webhook_url` | VARCHAR(255) | Yes | None | None | Webhook URL |
| `payload` | TEXT | No | None | None | Payload |
| `response` | TEXT | No | None | None | Response |
| `status` | VARCHAR(255) | No | Success, Failed | Success | Status |
| `owner` | VARCHAR(255) | No | User | None | Owner |
| `assigned_to` | VARCHAR(255) | No | User | None | Assigned To |
| `created_by` | VARCHAR(255) | No | User | None | Created By |
| `modified_by` | VARCHAR(255) | No | User | None | Modified By |
| `creation` | DATETIME | No | None | None | Creation |
| `modified` | DATETIME | No | None | None | Modified |
| `docstatus` | VARCHAR(255) | No | 0, 1, 2 | None | Docstatus |

---

## tabwhatsapp_conversation (whatsapp_conversation)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `phone_number` | VARCHAR(255) | Yes | None | None | Phone Number |
| `lead` | VARCHAR(255) | No | Lead | None | Lead |
| `status` | VARCHAR(255) | No | Open, Closed | Open | Status |
| `owner` | VARCHAR(255) | No | User | None | Owner |
| `assigned_to` | VARCHAR(255) | No | User | None | Assigned To |
| `created_by` | VARCHAR(255) | No | User | None | Created By |
| `modified_by` | VARCHAR(255) | No | User | None | Modified By |
| `creation` | DATETIME | No | None | None | Creation |
| `modified` | DATETIME | No | None | None | Modified |
| `docstatus` | VARCHAR(255) | No | 0, 1, 2 | None | Docstatus |
| `company` | VARCHAR(255) | No | Company | None | Company |
| `territory` | VARCHAR(255) | No | Territory | None | Territory |
| `team` | VARCHAR(255) | No | Team | None | Team |

---

## tabwhatsapp_message (whatsapp_message)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `conversation` | VARCHAR(255) | Yes | WhatsApp Conversation | None | Conversation |
| `direction` | VARCHAR(255) | Yes | Inbound, Outbound | Inbound | Direction |
| `message_type` | VARCHAR(255) | Yes | Text, Image, Document, Template | None | Message Type |
| `content` | TEXT | No | None | None | Content |
| `timestamp` | DATETIME | No | None | Now | Timestamp |
| `message_id` | VARCHAR(255) | No | None | None | Message ID |
| `owner` | VARCHAR(255) | No | User | None | Owner |
| `assigned_to` | VARCHAR(255) | No | User | None | Assigned To |
| `created_by` | VARCHAR(255) | No | User | None | Created By |
| `modified_by` | VARCHAR(255) | No | User | None | Modified By |
| `creation` | DATETIME | No | None | None | Creation |
| `modified` | DATETIME | No | None | None | Modified |
| `docstatus` | VARCHAR(255) | No | 0, 1, 2 | None | Docstatus |
| `company` | VARCHAR(255) | No | Company | None | Company |
| `territory` | VARCHAR(255) | No | Territory | None | Territory |
| `team` | VARCHAR(255) | No | Team | None | Team |

---

## tabworkflow_action (workflow_action)

| Field | Type | Required | Options | Default Value | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `name` | VARCHAR(255) | Yes | None | None | Standard system field |
| `owner` | VARCHAR(255) | Yes | None | Administrator | Standard system field |
| `creation` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified` | DATETIME(6) | Yes | None | None | Standard system field |
| `modified_by` | VARCHAR(255) | Yes | None | None | Standard system field |
| `docstatus` | INT(1) | Yes | None | 0 | Standard system field |
| `idx` | INT(8) | Yes | None | 0 | Standard system field |
| `action_name` | VARCHAR(255) | Yes | None | None | Action Name |
| `workflow_name` | VARCHAR(255) | Yes | None | None | Workflow Name |
| `allowed_role` | VARCHAR(255) | No | Role | None | Allowed Role |
| `owner` | VARCHAR(255) | No | User | None | Owner |
| `assigned_to` | VARCHAR(255) | No | User | None | Assigned To |
| `created_by` | VARCHAR(255) | No | User | None | Created By |
| `modified_by` | VARCHAR(255) | No | User | None | Modified By |
| `creation` | DATETIME | No | None | None | Creation |
| `modified` | DATETIME | No | None | None | Modified |
| `docstatus` | VARCHAR(255) | No | 0, 1, 2 | None | Docstatus |

---

