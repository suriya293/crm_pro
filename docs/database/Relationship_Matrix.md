# CRM Pro Schema Relationship Matrix

| Source Table | Target Table | Relationship Type |
| :--- | :--- | :--- |
| `tabCRM Contact` | `tabCRM Company` | Many-to-One |
| `tabCRM Deal` | `tabCRM Company` | Many-to-One |
| `tabCRM Contact Email` | `tabCRM Contact` | One-to-Many |
| `tabCRM Contact Phone` | `tabCRM Contact` | One-to-Many |
| `tabCRM Activity` | `tabCRM Deal` | Many-to-One |
| `tabCRM Attachment` | `tabCRM Deal` | Many-to-One |
| `tabCRM Note` | `tabCRM Deal` | Many-to-One |
| `tabCRM Task` | `tabCRM Deal` | Many-to-One |
| `tabCRM Activity` | `tabCRM Lead` | Many-to-One |
| `tabCRM Attachment` | `tabCRM Lead` | Many-to-One |
| `tabCRM Call Log` | `tabCRM Lead` | Many-to-One |
| `tabCRM Contact` | `tabCRM Lead` | Many-to-One |
| `tabCRM Custom Field` | `tabCRM Lead` | One-to-Many |
| `tabCRM Deal` | `tabCRM Lead` | Many-to-One |
| `tabCRM Email Log` | `tabCRM Lead` | Many-to-One |
| `tabCRM Meeting` | `tabCRM Lead` | Many-to-One |
| `tabCRM Note` | `tabCRM Lead` | Many-to-One |
| `tabCRM Reminder` | `tabCRM Lead` | Many-to-One |
| `tabCRM Task` | `tabCRM Lead` | Many-to-One |
| `tabCRM WhatsApp Log` | `tabCRM Lead` | Many-to-One |
| `tabCRM Pipeline Stage` | `tabCRM Pipeline` | Many-to-One |
| `tabCRM Settings` | `tabCRM Pipeline` | Many-to-One |
| `tabCRM Deal` | `tabCRM Pipeline Stage` | Many-to-One |
| `tabCRM Lead` | `tabCRM Pipeline Stage` | Many-to-One |
| `tabCRM Sales Target` | `tabCRM Team` | Many-to-One |
| `tabCRM User Profile` | `tabCRM Team` | Many-to-One |
| `tabfacebook_lead` | `tabCampaign` | Many-to-One |
| `tabactivity` | `tabCompany` | Many-to-One |
| `tabcampaign` | `tabCompany` | Many-to-One |
| `tabcompany` | `tabCompany` | Many-to-One |
| `tabcontact` | `tabCompany` | Many-to-One |
| `tabdeal` | `tabCompany` | Many-to-One |
| `tabdepartment` | `tabCompany` | Many-to-One |
| `tabfacebook_lead` | `tabCompany` | Many-to-One |
| `tabfollowup` | `tabCompany` | Many-to-One |
| `tabinvoice` | `tabCompany` | Many-to-One |
| `tablead_source` | `tabCompany` | Many-to-One |
| `tabopportunity` | `tabCompany` | Many-to-One |
| `tabpayment_entry` | `tabCompany` | Many-to-One |
| `tabprice_list` | `tabCompany` | Many-to-One |
| `tabproduct` | `tabCompany` | Many-to-One |
| `tabproduct_category` | `tabCompany` | Many-to-One |
| `tabquotation` | `tabCompany` | Many-to-One |
| `tabtask` | `tabCompany` | Many-to-One |
| `tabteam` | `tabCompany` | Many-to-One |
| `tabterritory` | `tabCompany` | Many-to-One |
| `tabwhatsapp_conversation` | `tabCompany` | Many-to-One |
| `tabwhatsapp_message` | `tabCompany` | Many-to-One |
| `tabinvoice` | `tabContact` | Many-to-One |
| `tabquotation` | `tabContact` | Many-to-One |
| `tabpayment_entry` | `tabInvoice` | Many-to-One |
| `tabactivity` | `tabLead` | Many-to-One |
| `tabcontact` | `tabLead` | Many-to-One |
| `tabfollowup` | `tabLead` | Many-to-One |
| `tabopportunity` | `tabLead` | Many-to-One |
| `tabtask` | `tabLead` | Many-to-One |
| `tabwhatsapp_conversation` | `tabLead` | Many-to-One |
| `tabdeal` | `tabOpportunity` | Many-to-One |
| `tabprice_list` | `tabProduct` | Many-to-One |
| `tabproduct` | `tabProduct Category` | Many-to-One |
| `tabworkflow_action` | `tabRole` | Many-to-One |
| `tabactivity` | `tabTeam` | Many-to-One |
| `tabcampaign` | `tabTeam` | Many-to-One |
| `tabcompany` | `tabTeam` | Many-to-One |
| `tabdeal` | `tabTeam` | Many-to-One |
| `tabfacebook_lead` | `tabTeam` | Many-to-One |
| `tabfollowup` | `tabTeam` | Many-to-One |
| `tabinvoice` | `tabTeam` | Many-to-One |
| `tablead_source` | `tabTeam` | Many-to-One |
| `tabopportunity` | `tabTeam` | Many-to-One |
| `tabpayment_entry` | `tabTeam` | Many-to-One |
| `tabprice_list` | `tabTeam` | Many-to-One |
| `tabproduct` | `tabTeam` | Many-to-One |
| `tabproduct_category` | `tabTeam` | Many-to-One |
| `tabquotation` | `tabTeam` | Many-to-One |
| `tabtask` | `tabTeam` | Many-to-One |
| `tabwhatsapp_conversation` | `tabTeam` | Many-to-One |
| `tabwhatsapp_message` | `tabTeam` | Many-to-One |
| `tabactivity` | `tabTerritory` | Many-to-One |
| `tabcampaign` | `tabTerritory` | Many-to-One |
| `tabcompany` | `tabTerritory` | Many-to-One |
| `tabdeal` | `tabTerritory` | Many-to-One |
| `tabfacebook_lead` | `tabTerritory` | Many-to-One |
| `tabfollowup` | `tabTerritory` | Many-to-One |
| `tabinvoice` | `tabTerritory` | Many-to-One |
| `tablead_source` | `tabTerritory` | Many-to-One |
| `tabopportunity` | `tabTerritory` | Many-to-One |
| `tabpayment_entry` | `tabTerritory` | Many-to-One |
| `tabprice_list` | `tabTerritory` | Many-to-One |
| `tabproduct` | `tabTerritory` | Many-to-One |
| `tabproduct_category` | `tabTerritory` | Many-to-One |
| `tabquotation` | `tabTerritory` | Many-to-One |
| `tabtask` | `tabTerritory` | Many-to-One |
| `tabwhatsapp_conversation` | `tabTerritory` | Many-to-One |
| `tabwhatsapp_message` | `tabTerritory` | Many-to-One |
| `tabCRM Audit Log` | `tabUser` | Many-to-One |
| `tabCRM Lead` | `tabUser` | Many-to-One |
| `tabCRM Note` | `tabUser` | Many-to-One |
| `tabCRM Notification` | `tabUser` | Many-to-One |
| `tabCRM Reminder` | `tabUser` | Many-to-One |
| `tabCRM Sales Target` | `tabUser` | Many-to-One |
| `tabCRM Task` | `tabUser` | Many-to-One |
| `tabCRM Team` | `tabUser` | Many-to-One |
| `tabCRM User Profile` | `tabUser` | Many-to-One |
| `tabactivity` | `tabUser` | Many-to-One |
| `tabactivity` | `tabUser` | Many-to-One |
| `tabactivity` | `tabUser` | Many-to-One |
| `tabactivity` | `tabUser` | Many-to-One |
| `tabactivity` | `tabUser` | Many-to-One |
| `tabapi_log` | `tabUser` | Many-to-One |
| `tabapi_log` | `tabUser` | Many-to-One |
| `tabapi_log` | `tabUser` | Many-to-One |
| `tabapi_log` | `tabUser` | Many-to-One |
| `tabapi_log` | `tabUser` | Many-to-One |
| `tabaudit_log` | `tabUser` | Many-to-One |
| `tabaudit_log` | `tabUser` | Many-to-One |
| `tabaudit_log` | `tabUser` | Many-to-One |
| `tabaudit_log` | `tabUser` | Many-to-One |
| `tabaudit_log` | `tabUser` | Many-to-One |
| `tabautomation_rule` | `tabUser` | Many-to-One |
| `tabautomation_rule` | `tabUser` | Many-to-One |
| `tabautomation_rule` | `tabUser` | Many-to-One |
| `tabautomation_rule` | `tabUser` | Many-to-One |
| `tabcampaign` | `tabUser` | Many-to-One |
| `tabcampaign` | `tabUser` | Many-to-One |
| `tabcampaign` | `tabUser` | Many-to-One |
| `tabcampaign` | `tabUser` | Many-to-One |
| `tabcompany` | `tabUser` | Many-to-One |
| `tabcompany` | `tabUser` | Many-to-One |
| `tabcompany` | `tabUser` | Many-to-One |
| `tabcompany` | `tabUser` | Many-to-One |
| `tabcompany` | `tabUser` | Many-to-One |
| `tabdeal` | `tabUser` | Many-to-One |
| `tabdeal` | `tabUser` | Many-to-One |
| `tabdeal` | `tabUser` | Many-to-One |
| `tabdeal` | `tabUser` | Many-to-One |
| `tabdepartment` | `tabUser` | Many-to-One |
| `tabdepartment` | `tabUser` | Many-to-One |
| `tabdepartment` | `tabUser` | Many-to-One |
| `tabdepartment` | `tabUser` | Many-to-One |
| `tabexport_job` | `tabUser` | Many-to-One |
| `tabexport_job` | `tabUser` | Many-to-One |
| `tabexport_job` | `tabUser` | Many-to-One |
| `tabexport_job` | `tabUser` | Many-to-One |
| `tabfacebook_lead` | `tabUser` | Many-to-One |
| `tabfacebook_lead` | `tabUser` | Many-to-One |
| `tabfacebook_lead` | `tabUser` | Many-to-One |
| `tabfacebook_lead` | `tabUser` | Many-to-One |
| `tabfollowup` | `tabUser` | Many-to-One |
| `tabfollowup` | `tabUser` | Many-to-One |
| `tabfollowup` | `tabUser` | Many-to-One |
| `tabfollowup` | `tabUser` | Many-to-One |
| `tabimport_job` | `tabUser` | Many-to-One |
| `tabimport_job` | `tabUser` | Many-to-One |
| `tabimport_job` | `tabUser` | Many-to-One |
| `tabimport_job` | `tabUser` | Many-to-One |
| `tabinvoice` | `tabUser` | Many-to-One |
| `tabinvoice` | `tabUser` | Many-to-One |
| `tabinvoice` | `tabUser` | Many-to-One |
| `tabinvoice` | `tabUser` | Many-to-One |
| `tablead` | `tabUser` | Many-to-One |
| `tablead_source` | `tabUser` | Many-to-One |
| `tablead_source` | `tabUser` | Many-to-One |
| `tablead_source` | `tabUser` | Many-to-One |
| `tablead_source` | `tabUser` | Many-to-One |
| `tabnotification` | `tabUser` | Many-to-One |
| `tabnotification` | `tabUser` | Many-to-One |
| `tabnotification` | `tabUser` | Many-to-One |
| `tabnotification` | `tabUser` | Many-to-One |
| `tabnotification` | `tabUser` | Many-to-One |
| `tabopportunity` | `tabUser` | Many-to-One |
| `tabopportunity` | `tabUser` | Many-to-One |
| `tabopportunity` | `tabUser` | Many-to-One |
| `tabopportunity` | `tabUser` | Many-to-One |
| `tabpayment_entry` | `tabUser` | Many-to-One |
| `tabpayment_entry` | `tabUser` | Many-to-One |
| `tabpayment_entry` | `tabUser` | Many-to-One |
| `tabpayment_entry` | `tabUser` | Many-to-One |
| `tabprice_list` | `tabUser` | Many-to-One |
| `tabprice_list` | `tabUser` | Many-to-One |
| `tabprice_list` | `tabUser` | Many-to-One |
| `tabprice_list` | `tabUser` | Many-to-One |
| `tabproduct` | `tabUser` | Many-to-One |
| `tabproduct` | `tabUser` | Many-to-One |
| `tabproduct` | `tabUser` | Many-to-One |
| `tabproduct` | `tabUser` | Many-to-One |
| `tabproduct_category` | `tabUser` | Many-to-One |
| `tabproduct_category` | `tabUser` | Many-to-One |
| `tabproduct_category` | `tabUser` | Many-to-One |
| `tabproduct_category` | `tabUser` | Many-to-One |
| `tabquotation` | `tabUser` | Many-to-One |
| `tabquotation` | `tabUser` | Many-to-One |
| `tabquotation` | `tabUser` | Many-to-One |
| `tabquotation` | `tabUser` | Many-to-One |
| `tabtask` | `tabUser` | Many-to-One |
| `tabtask` | `tabUser` | Many-to-One |
| `tabtask` | `tabUser` | Many-to-One |
| `tabtask` | `tabUser` | Many-to-One |
| `tabtask` | `tabUser` | Many-to-One |
| `tabteam` | `tabUser` | Many-to-One |
| `tabteam` | `tabUser` | Many-to-One |
| `tabteam` | `tabUser` | Many-to-One |
| `tabteam` | `tabUser` | Many-to-One |
| `tabteam` | `tabUser` | Many-to-One |
| `tabterritory` | `tabUser` | Many-to-One |
| `tabterritory` | `tabUser` | Many-to-One |
| `tabterritory` | `tabUser` | Many-to-One |
| `tabterritory` | `tabUser` | Many-to-One |
| `tabwebhook_log` | `tabUser` | Many-to-One |
| `tabwebhook_log` | `tabUser` | Many-to-One |
| `tabwebhook_log` | `tabUser` | Many-to-One |
| `tabwebhook_log` | `tabUser` | Many-to-One |
| `tabwhatsapp_conversation` | `tabUser` | Many-to-One |
| `tabwhatsapp_conversation` | `tabUser` | Many-to-One |
| `tabwhatsapp_conversation` | `tabUser` | Many-to-One |
| `tabwhatsapp_conversation` | `tabUser` | Many-to-One |
| `tabwhatsapp_message` | `tabUser` | Many-to-One |
| `tabwhatsapp_message` | `tabUser` | Many-to-One |
| `tabwhatsapp_message` | `tabUser` | Many-to-One |
| `tabwhatsapp_message` | `tabUser` | Many-to-One |
| `tabworkflow_action` | `tabUser` | Many-to-One |
| `tabworkflow_action` | `tabUser` | Many-to-One |
| `tabworkflow_action` | `tabUser` | Many-to-One |
| `tabworkflow_action` | `tabUser` | Many-to-One |
| `tabwhatsapp_message` | `tabWhatsApp Conversation` | Many-to-One |
