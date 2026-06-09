// config.js provides centralized configuration for the LeadsCRM application.
export const CONFIG = {
  // Backend Frappe server URL
  backendUrl: process.env.FRP_BASE_URL || "http://localhost:8000",
  // API Authorization token for backend
  apiToken: process.env.FRP_AUTH_TOKEN || "",
  // WhatsApp integration tokens
  whatsappPhoneNumberId: process.env.WHATSAPP_PHONE_NUMBER_ID || "",
  whatsappAccessToken: process.env.WHATSAPP_ACCESS_TOKEN || "",
  whatsappVerifyToken: process.env.WHATSAPP_VERIFY_TOKEN || "",
  // Facebook integration tokens
  facebookAccessToken: process.env.FB_ACCESS_TOKEN || "",
  facebookAppSecret: process.env.FB_APP_SECRET || "",
  facebookVerifyToken: process.env.FB_VERIFY_TOKEN || "",
  // Storage key for UI settings
  settingsStorageKey: "leadscrm_settings"
};
export default CONFIG;
