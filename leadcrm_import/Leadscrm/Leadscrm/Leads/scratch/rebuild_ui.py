import os

js_path = r"c:\Users\YUVEHA\OneDrive\Documents\Leads\scratch\current_js.txt"
with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# Make sure we don't duplicate <script> if it's already there
if not js_content.strip().startswith("<script>"):
    js_content = "<script>\n" + js_content
if not js_content.strip().endswith("</script>"):
    js_content = js_content + "\n</script>"

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>LEADS CRM</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet"/>
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        'primary': '#6a9df5',
                        'primary-light': '#b5cfff',
                        'primary-dark': '#558AF2',
                        'bg-main': '#f2f6fa',
                        'text-dark': '#334155',
                        'text-light': '#64748b',
                    },
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                    }
                }
            }
        }
    </script>
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #f2f6fa; }
        .material-symbols-outlined { font-size: 18px; }
        
        /* Scrollbar */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background-color: #cbd5e1; border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background-color: #94a3b8; }
        
        .kanban-view {
            display: flex;
            overflow-x: auto;
            overflow-y: hidden;
            flex: 1;
            padding: 1rem;
            gap: 1rem;
        }
        .kanban-column {
            width: 320px;
            flex-shrink: 0;
            display: flex;
            flex-direction: column;
            background: transparent;
            border-radius: 8px;
        }
        .chevron-header {
            background-color: #8ab4f8;
            color: white;
            padding: 10px 16px;
            padding-right: 24px;
            clip-path: polygon(0 0, calc(100% - 16px) 0, 100% 50%, calc(100% - 16px) 100%, 0 100%);
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-weight: 700;
            font-size: 13px;
        }
        .kanban-subheader {
            background-color: white;
            padding: 8px 16px;
            font-size: 11px;
            color: #64748b;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            align-items: center;
            gap: 4px;
        }
        .kanban-cards-container {
            flex: 1;
            overflow-y: auto;
            padding: 8px 0;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .lead-card {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 12px;
            display: flex;
            flex-direction: column;
            gap: 8px;
            font-size: 12px;
            color: #64748b;
        }
        .lead-card-row {
            display: flex;
            justify-content: space-between;
        }
        .lead-card-value {
            color: #334155;
            font-weight: 500;
            text-align: right;
        }
        .action-icon {
            color: #64748b;
            cursor: pointer;
            transition: color 0.2s;
            font-size: 16px;
        }
        .action-icon:hover { color: #3b82f6; }
        
        .contact-icons {
            display: flex;
            gap: 6px;
            justify-content: flex-end;
            margin-top: 4px;
        }
        .contact-btn {
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            background: transparent;
        }
        .contact-btn .material-symbols-outlined {
            font-size: 18px;
        }
        .badge {
            position: absolute;
            top: -4px;
            right: -6px;
            background: #ef4444;
            color: white;
            font-size: 9px;
            font-weight: bold;
            border-radius: 999px;
            width: 14px;
            height: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            line-height: 1;
        }
        
        .pill-btn {
            background-color: #8ab4f8;
            color: white;
            border-radius: 9999px;
            padding: 6px 16px;
            font-size: 12px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 4px;
            white-space: nowrap;
        }
        .pill-btn.primary {
            background-color: #6a9df5;
        }
    </style>
</head>
<body class="flex h-screen overflow-hidden">

<!-- Sidebar -->
<aside class="w-64 bg-primary text-white flex flex-col flex-shrink-0">
    <div class="p-6">
        <h1 class="text-2xl font-bold tracking-wider">LEADS</h1>
        <p class="text-[10px] font-semibold uppercase tracking-wider opacity-90 mt-1">CRM ADMIN</p>
    </div>
    
    <nav class="flex-1 px-4 space-y-2 mt-4">
        <a href="code.html" class="flex items-center gap-3 px-4 py-3 bg-white/20 rounded-xl transition-colors">
            <span class="material-symbols-outlined text-[20px]">sort</span>
            <span class="font-semibold text-sm">Leads</span>
        </a>
        <a href="settings.html" class="flex items-center gap-3 px-4 py-3 hover:bg-white/10 rounded-xl transition-colors">
            <span class="material-symbols-outlined text-[20px]">settings</span>
            <span class="font-semibold text-sm">Settings</span>
        </a>
    </nav>
    
    <div class="p-4 space-y-2 mb-2">
        <button class="w-full flex items-center gap-3 px-4 py-3 bg-[#8ab4f8] hover:bg-[#7ba8f5] rounded-xl transition-colors text-sm font-semibold">
            <span class="material-symbols-outlined text-[20px]">help_outline</span> Help
        </button>
        <button class="w-full flex items-center gap-3 px-4 py-3 bg-[#8ab4f8] hover:bg-[#7ba8f5] rounded-xl transition-colors text-sm font-semibold">
            <span class="material-symbols-outlined text-[20px]">logout</span> Logout
        </button>
    </div>
</aside>

<!-- Main Content -->
<main class="flex-1 flex flex-col min-w-0 bg-bg-main">
    
    <!-- Header -->
    <header class="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6 shrink-0">
        <h2 class="text-xl font-bold text-primary tracking-wide">LEADS</h2>
        
        <div class="flex items-center gap-5">
            <div class="flex items-center gap-1.5 text-slate-500 text-sm font-medium">
                <span class="material-symbols-outlined text-[18px]">schedule</span>
                <span id="live-clock">--:--:--</span>
            </div>
            
            <div class="flex items-center gap-3 text-slate-600">
                <button class="hover:text-primary"><span class="material-symbols-outlined">lightbulb</span></button>
                <button onclick="toggleFullscreen()"><span class="material-symbols-outlined">fullscreen</span></button>
                <button class="hover:text-primary"><span class="material-symbols-outlined">dark_mode</span></button>
                <button class="relative hover:text-primary">
                    <span class="material-symbols-outlined">notifications</span>
                    <span class="absolute -top-1 -right-1 bg-red-500 text-white text-[10px] w-4 h-4 rounded-full flex items-center justify-center font-bold">3</span>
                </button>
            </div>
            
            <button class="flex items-center gap-2 bg-slate-50 border border-slate-200 rounded-full py-1.5 px-3 hover:bg-slate-100 transition-colors">
                <div class="w-6 h-6 bg-primary rounded-full flex items-center justify-center text-white text-[12px] font-bold">
                    <span class="material-symbols-outlined text-[14px]">person</span>
                </div>
                <span class="text-sm font-semibold text-slate-700">Admin</span>
                <span class="material-symbols-outlined text-[16px] text-slate-400">expand_more</span>
            </button>
        </div>
    </header>

    <!-- Toolbar -->
    <div class="bg-white border-b border-slate-200 px-6 py-3 flex items-center justify-between gap-4 shrink-0 overflow-x-auto hide-scrollbar">
        <div class="flex items-center gap-3">
            <button class="pill-btn">Grid View <span class="material-symbols-outlined text-[16px]">expand_more</span></button>
            <button class="pill-btn">Created Date <span class="material-symbols-outlined text-[16px]">expand_more</span></button>
            <button class="pill-btn">Descending <span class="material-symbols-outlined text-[16px]">expand_more</span></button>
            <button class="pill-btn">Status: All <span class="material-symbols-outlined text-[16px]">expand_more</span></button>
        </div>
        
        <div class="flex items-center gap-3">
            <div class="relative w-48">
                <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-[18px]">search</span>
                <input id="search-leads-input" oninput="handleSearchLeads(this.value)" class="w-full pl-9 pr-3 py-1.5 rounded-full border border-slate-200 focus:outline-none focus:border-primary text-sm" placeholder="Search leads..." type="text"/>
            </div>
            
            <button class="pill-btn">Integration</button>
            <button class="pill-btn">Import</button>
            <button class="pill-btn">Import History</button>
            
            <button class="pill-btn primary ml-2 shadow-sm shadow-blue-200 hover:bg-primary-dark transition-colors" onclick="openAddLeadModal()">
                <span class="material-symbols-outlined text-[16px]">add</span> Add Lead
            </button>
            <button class="w-8 h-8 rounded-full bg-primary text-white flex items-center justify-center shadow-sm shadow-blue-200 hover:bg-primary-dark transition-colors" onclick="handleRefreshLeads()">
                <span class="material-symbols-outlined text-[16px]">refresh</span>
            </button>
        </div>
    </div>

    <!-- Kanban Board -->
    <div class="kanban-view" id="kanban-view-container">
        <!-- Injected via JS -->
    </div>
</main>

<!-- Modals -->
<div id="lead-modal" class="hidden fixed inset-0 bg-slate-900/40 z-50 flex items-center justify-center p-4">
    <!-- Simplified modal content for matching functionality -->
    <div class="bg-white rounded-xl shadow-xl w-full max-w-lg p-6">
        <h3 id="modal-title" class="text-lg font-bold text-slate-800 mb-4">Add Lead</h3>
        <p class="text-sm text-slate-500 mb-4">Add your lead details here.</p>
        <div class="flex justify-end gap-2">
            <button onclick="closeLeadModal()" class="px-4 py-2 bg-slate-100 rounded-lg text-sm font-semibold text-slate-700">Close</button>
        </div>
    </div>
</div>

""" + js_content + """
<script>
// Live clock
setInterval(() => {
    const el = document.getElementById('live-clock');
    if(el) {
        const d = new Date();
        el.textContent = d.toLocaleString('en-GB').replace(',', '');
    }
}, 1000);

function toggleFullscreen() {
    if (!document.fullscreenElement) document.documentElement.requestFullscreen();
    else if (document.exitFullscreen) document.exitFullscreen();
}

// Override JS render functions to match the requested design
function renderLeads() {
    const container = document.getElementById('kanban-view-container');
    if(!container) return;
    
    // The columns ordered
    const stages = ['LEAD', 'LOST', 'FOLLOW UP', 'PROPOSAL SENT', 'OTHERS', 'HOT', 'TRIAL AC', 'ONBOARDED', 'DEMO DONE', 'RNR', 'CALL BACK', 'INVOICE', 'DEMO SCHEDULE'];
    
    container.innerHTML = '';
    
    stages.forEach(stage => {
        let stageLeads = leadsData.filter(l => l.stage === stage);
        if (statusFilter !== 'All' && statusFilter !== stage) return;
        
        // Filter by search
        if (searchQuery) {
            const q = searchQuery.toLowerCase();
            stageLeads = stageLeads.filter(l => (l.name||'').toLowerCase().includes(q) || (l.mobile||'').toLowerCase().includes(q));
        }
        
        // Calculate amount (mocked sum for now)
        const totalAmount = stageLeads.reduce((sum, l) => sum + (parseFloat(l.amount) || 0), 0);
        
        let html = 
        <div class="kanban-column">
            <header class="chevron-header">
                <div class="flex items-center gap-1.5">
                    <span class="material-symbols-outlined text-[16px] bg-white text-primary rounded-full w-5 h-5 flex items-center justify-center">error</span>
                    <span></span>
                </div>
                <span class="material-symbols-outlined cursor-pointer hover:bg-white/20 rounded-full p-0.5 text-[16px]" onclick="openAddLeadModal()">add</span>
            </header>
            <div class="kanban-subheader">
                <span>&#8377; </span>
                <span class="px-1">•</span>
                <span> lead</span>
            </div>
            <div class="kanban-cards-container">
        ;
        
        stageLeads.forEach(lead => {
            const safeName = lead.name.replace(/'/g, "\\'");
            
            html += 
            <div class="lead-card hover:shadow-md transition-shadow cursor-pointer">
                <div class="flex justify-between items-start mb-1">
                    <h4 class="font-bold text-[13px] text-slate-800"></h4>
                    <div class="flex gap-1.5 text-primary">
                        <span class="material-symbols-outlined action-icon text-[16px]" onclick="openEditLeadModal('')">edit</span>
                        <span class="material-symbols-outlined action-icon text-[16px]" onclick="deleteLead('')">delete</span>
                    </div>
                </div>
                
                <div class="lead-card-row">
                    <span>Email:</span>
                    <span class="lead-card-value"></span>
                </div>
                <div class="lead-card-row items-center">
                    <span>Mobile: </span>
                    <div class="contact-icons">
                        <div class="contact-btn text-green-500">
                            <span class="material-symbols-outlined">call</span>
                            <span class="badge"></span>
                        </div>
                        <div class="contact-btn text-yellow-500">
                            <span class="material-symbols-outlined">chat_bubble</span>
                            <span class="badge"></span>
                        </div>
                        <div class="contact-btn text-green-600">
                            <span class="material-symbols-outlined">forum</span>
                            <span class="badge"></span>
                        </div>
                    </div>
                </div>
                <div class="lead-card-row mt-1">
                    <span>Status:</span>
                    <span class="lead-card-value"></span>
                </div>
                <div class="lead-card-row">
                    <span>Source:</span>
                    <span class="lead-card-value"></span>
                </div>
                <div class="lead-card-row">
                    <span>Assign:</span>
                    <span class="lead-card-value"></span>
                </div>
                
                <hr class="border-slate-100 my-1"/>
                
                <div class="lead-card-row">
                    <span>Amount:</span>
                    <span class="lead-card-value"></span>
                </div>
                <div class="lead-card-row">
                    <span>Priority:</span>
                    <span class="lead-card-value"></span>
                </div>
                <div class="lead-card-row">
                    <span>Completed Date:</span>
                    <span class="lead-card-value"></span>
                </div>
                <div class="lead-card-row">
                    <span>Creation Date:</span>
                    <span class="lead-card-value"></span>
                </div>
            </div>
            ;
        });
        
        html += 
            </div>
        </div>
        ;
        
        container.insertAdjacentHTML('beforeend', html);
    });
}

// Initial render
window.onload = () => {
    if(typeof loadLeadsData === 'function') loadLeadsData();
    if(typeof renderLeads === 'function') renderLeads();
};

function handleSearchLeads(val) {
    searchQuery = val;
    renderLeads();
}
function handleRefreshLeads() {
    renderLeads();
}
</script>
</body>
</html>
"""

with open(r"c:\Users\YUVEHA\OneDrive\Documents\Leads\code.html", "w", encoding="utf-8", newline="\r\n") as f:
    f.write(html_content)

print("Rebuild UI completed!")
