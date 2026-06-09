// LeadsCRM Backend Connector (crm_api.js)

import { CONFIG as CRM_CONFIG } from "./config.js";

/**
 * Checks if a backend is configured
 */
function isBackendEnabled() {
    return !!CRM_CONFIG.backendUrl && CRM_CONFIG.backendUrl.trim() !== '';
}

/**
 * Performs whitelisted requests to Frappe backend
 */
async function crmRequest(method, args = {}) {
    if (!isBackendEnabled()) {
        throw new Error("No backend configured. Using local fallback.");
    }

    let baseUrl = CRM_CONFIG.backendUrl.trim();
    if (baseUrl.endsWith('/')) {
        baseUrl = baseUrl.slice(0, -1);
    }
    const url = `${baseUrl}/api/method/${method}`;
    const headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    };

    if (CRM_CONFIG.apiToken) {
        let token = CRM_CONFIG.apiToken.trim();
        if (token && !token.startsWith("token ") && !token.startsWith("Bearer ") && !token.startsWith("Basic ")) {
            token = "Bearer " + token;
        }
        headers["Authorization"] = token;
    }

    const response = await fetch(url, {
        method: "POST",
        headers: headers,
        body: JSON.stringify(args)
    });

    if (!response.ok) {
        const errText = await response.text();
        throw new Error(`API Error: ${response.status} - ${errText}`);
    }

    const data = await response.json();
    return data.message;
}

// Helper to format dates consistently with the frontend format (DD-MMM-YYYY HH:MM)
function formatDate(dateStr) {
    if (!dateStr) return '-';
    try {
        const d = new Date(dateStr.replace(' ', 'T'));
        return d.toLocaleDateString('en-IN', { day:'2-digit', month:'short', year:'numeric', hour:'2-digit', minute:'2-digit' });
    } catch(e) {
        return dateStr;
    }
}

// Helper to normalize lead fields returned by the backend
function normalizeLeadFromBackend(lead) {
    if (!lead) return null;
    return {
        ...lead,
        name: lead.lead_name || lead.name,
        db_id: lead.name,
        creationDate: formatDate(lead.creation),
        modifiedDate: formatDate(lead.modified),
        followupDate: lead.followup_date ? formatDate(lead.followup_date) : '-',
        amount: lead.value || lead.opportunity_value || 0,
        company: lead.company || '-',
        callsCount: lead.callsCount || 0,
        smsCount: lead.smsCount || 0,
        whatsappCount: lead.whatsappCount || 0
    };
}

// ==========================================
// LEAD API WRAPPERS
// ==========================================

export async function apiGetLeads(filters = {}) {
    if (isBackendEnabled()) {
        try {
            const res = await crmRequest("precision_crm.precision_crm.api.leads.list_leads", {
                filters: JSON.stringify(filters)
            });
            if (res && res.status === "success") {
                return (res.data || []).map(normalizeLeadFromBackend);
            }
        } catch (e) {
            console.error("Backend failed. Falling back to local storage.", e);
        }
    }
    return JSON.parse(localStorage.getItem('leadsData') || '[]');
}

export async function apiGetLead(name) {
    if (isBackendEnabled()) {
        try {
            const res = await crmRequest("precision_crm.precision_crm.api.leads.get_lead", {
                name: name
            });
            if (res && res.status === "success") {
                return normalizeLeadFromBackend(res.data);
            }
        } catch (e) {
            console.error("Backend failed. Falling back to local storage.", e);
        }
    }
    const leads = JSON.parse(localStorage.getItem('leadsData') || '[]');
    return leads.find(l => l.name === name) || null;
}

export async function apiCreateLead(leadData) {
    if (isBackendEnabled()) {
        try {
            const res = await crmRequest("precision_crm.precision_crm.api.leads.create_lead", leadData);
            if (res && res.status === "success") {
                return res.data.name;
            }
        } catch (e) {
            console.error("Backend failed. Falling back to local storage.", e);
        }
    }
    
    // Local fallback
    const leads = JSON.parse(localStorage.getItem('leadsData') || '[]');
    const id = "lead_" + Date.now();
    const newLead = { name: id, ...leadData, creationDate: new Date().toLocaleDateString() };
    leads.push(newLead);
    localStorage.setItem('leadsData', JSON.stringify(leads));
    return id;
}

export async function apiUpdateLead(name, leadData) {
    if (isBackendEnabled()) {
        try {
            const res = await crmRequest("precision_crm.precision_crm.api.leads.update_lead", {
                name: name,
                ...leadData
            });
            if (res && res.status === "success") {
                return res.data.name;
            }
        } catch (e) {
            console.error("Backend failed. Falling back to local storage.", e);
        }
    }

    // Local fallback
    const leads = JSON.parse(localStorage.getItem('leadsData') || '[]');
    const idx = leads.findIndex(l => l.name === name);
    if (idx !== -1) {
        leads[idx] = { ...leads[idx], ...leadData, modifiedDate: new Date().toLocaleDateString() };
        localStorage.setItem('leadsData', JSON.stringify(leads));
    }
    return name;
}

export async function apiDeleteLead(name) {
    if (isBackendEnabled()) {
        try {
            const res = await crmRequest("precision_crm.precision_crm.api.leads.delete_lead", { name: name });
            if (res && res.status === "success") {
                return { status: "success" };
            }
        } catch (e) {
            console.error("Backend failed. Falling back to local storage.", e);
        }
    }

    // Local fallback
    let leads = JSON.parse(localStorage.getItem('leadsData') || '[]');
    leads = leads.filter(l => l.name !== name);
    localStorage.setItem('leadsData', JSON.stringify(leads));
    return { status: "success" };
}

// ==========================================
// METADATA & INTEGRATIONS
// ==========================================

export async function apiSendWhatsApp(leadId, message) {
    if (isBackendEnabled()) {
        // Find Lead Mobile Number
        const lead = await apiGetLead(leadId);
        if (lead && lead.mobile_no) {
            return await crmRequest("precision_crm.precision_crm.integrations.whatsapp_service.send_whatsapp_message", {
                to_number: lead.mobile_no,
                text_content: message
            });
        }
    } else {
        alert(`Local Mock: WhatsApp message sent to {leadId}: "${message}"`);
        return { status: "mocked" };
    }
}

export async function apiSaveSettings(settingsData) {
    let mergedData = {};
    try {
        mergedData = JSON.parse(localStorage.getItem('crmSettingsData') || '{}');
    } catch(e) {}
    mergedData = { ...mergedData, ...settingsData };
    localStorage.setItem('crmSettingsData', JSON.stringify(mergedData));
    return { status: "success" };
}

export async function apiGetSettings() {
    let localSettings = {};
    try {
        localSettings = JSON.parse(localStorage.getItem('crmSettingsData') || '{}');
    } catch (e) {}
    return localSettings;
}

// ==========================================
// CONFIG & SETTINGS SYNC (STAGES, SOURCES, USERS)
// ==========================================

export async function apiGetStages() {
    return JSON.parse(localStorage.getItem('leadStagesData') || '[]');
}

export async function apiSaveStages(stagesList) {
    localStorage.setItem('leadStagesData', JSON.stringify(stagesList));
}

export async function apiGetSources() {
    return JSON.parse(localStorage.getItem('leadSourcesData') || '[]');
}

export async function apiSaveSources(sourcesList) {
    localStorage.setItem('leadSourcesData', JSON.stringify(sourcesList));
}

export async function apiGetUsers() {
    return JSON.parse(localStorage.getItem('leadUsersData') || '[]');
}

export async function apiSaveUsers(usersList) {
    localStorage.setItem('leadUsersData', JSON.stringify(usersList));
}

// ==========================================
// NOTES & TASKS & TIMELINE API WRAPPERS
// ==========================================

export async function apiGetNotes(leadId) {
    return JSON.parse(localStorage.getItem(`crm_notes_${leadId}`) || '[]');
}

export async function apiCreateNote(leadId, content) {
    const notes = JSON.parse(localStorage.getItem(`crm_notes_${leadId}`) || '[]');
    const newNote = {
        id: "note_" + Date.now(),
        createdDate: new Date().toLocaleDateString('en-IN'),
        user: "Admin",
        content: content
    };
    notes.push(newNote);
    localStorage.setItem(`crm_notes_${leadId}`, JSON.stringify(notes));
    return newNote.id;
}

export async function apiDeleteNote(leadId, noteId) {
    let notes = JSON.parse(localStorage.getItem(`crm_notes_${leadId}`) || '[]');
    notes = notes.filter(n => n.id !== noteId);
    localStorage.setItem(`crm_notes_${leadId}`, JSON.stringify(notes));
}

export async function apiGetTasks(leadId) {
    if (isBackendEnabled()) {
        try {
            const res = await crmRequest("precision_crm.precision_crm.api.tasks.list_tasks", {
                filters: JSON.stringify({ related_lead: leadId })
            });
            if (res && res.status === "success") {
                return (res.data || []).map(t => ({
                    id: t.name,
                    dueDate: t.due_date || '-',
                    subject: t.task_name,
                    assignedTo: t.assignee || '-',
                    status: t.status || 'Open'
                }));
            }
        } catch (e) {
            console.error("Backend get_tasks failed.", e);
        }
    }
    return JSON.parse(localStorage.getItem(`crm_tasks_${leadId}`) || '[]');
}

export async function apiCreateTask(leadId, taskData) {
    if (isBackendEnabled()) {
        try {
            const res = await crmRequest("precision_crm.precision_crm.api.tasks.create_task", {
                related_lead: leadId,
                task_name: taskData.subject,
                due_date: taskData.dueDate,
                status: taskData.status || 'Open',
                assignee: taskData.assignedTo || 'Administrator'
            });
            if (res && res.status === "success") {
                return res.data.name;
            }
        } catch (e) {
            console.error("Backend create_task failed.", e);
        }
    }
    const tasks = JSON.parse(localStorage.getItem(`crm_tasks_${leadId}`) || '[]');
    const newTask = {
        id: "task_" + Date.now(),
        ...taskData
    };
    tasks.push(newTask);
    localStorage.setItem(`crm_tasks_${leadId}`, JSON.stringify(tasks));
    return newTask.id;
}

export async function apiDeleteTask(leadId, taskId) {
    if (isBackendEnabled()) {
        try {
            const res = await crmRequest("precision_crm.precision_crm.api.tasks.delete_task", { name: taskId });
            if (res && res.status === "success") {
                return { status: "success" };
            }
        } catch (e) {
            console.error("Backend delete_task failed.", e);
        }
    }
    let tasks = JSON.parse(localStorage.getItem(`crm_tasks_${leadId}`) || '[]');
    tasks = tasks.filter(t => t.id !== taskId);
    localStorage.setItem(`crm_tasks_${leadId}`, JSON.stringify(tasks));
}
