# Precision CRM

Precision CRM is an enterprise-grade Customer Relationship Management (CRM) application built on the Frappe v15 Framework. It provides robust capabilities for managing leads, contacts, deals, activities, and communication pipelines with automated integrations.

## Features

- **Lead & Contact Management**: Auto-escalation of stale leads, duplicate detection, round-robin assignment, and lead-to-contact conversion.
- **Deals & Sales Pipelines**: Track deal stages, amounts, and expected closing dates.
- **Integrations**:
  - **WhatsApp**: Sync incoming and outgoing WhatsApp messages, manage WhatsApp conversations.
  - **Facebook Lead Ads**: Webhook listener to automatically ingest Facebook leads and convert them programmatically.
- **Automation Engine**: Escalations, round-robin lead allocation, and task/follow-up reminders.
- **Analytics & Reporting**: Pipeline summaries, lead funnel analysis, campaign ROI, agent performance reports, and WhatsApp activity stats.

## Installation

1. Clone or copy the repository into your bench's `apps` folder.
2. Install the app on your bench site:
   ```bash
   bench get-app precision_crm /path/to/precision_crm
   bench --site <your-site> install-app precision_crm
   bench --site <your-site> migrate
   ```

## License

This project is licensed under the MIT License - see the `license.txt` file for details.
