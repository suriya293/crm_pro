import os

# Paths
work_dir = r"c:\Users\YUVEHA\OneDrive\Documents\Leads"
temp_script_path = os.path.join(work_dir, "scratch", "temp_script.js")
code_html_path = os.path.join(work_dir, "code.html")

# 1. Read temp_script.js content
with open(temp_script_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# 2. Build code.html content
html_content = """<!DOCTYPE html>
<html class="light" lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Leads - Grid View</title>
    <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap" rel="stylesheet"/>
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
    <script id="tailwind-config">
        tailwind.config = {
            theme: {
                extend: {
                    "colors": {
                        "on-primary": "#ffffff",
                        "surface-dim": "#bfdbfe",
                        "on-error-container": "#93000a",
                        "surface-container-lowest": "#ffffff",
                        "surface-container": "#dbeafe",
                        "on-secondary-container": "#1e40af",
                        "outline-variant": "#cbd5e1",
                        "surface-bright": "#f8faff",
                        "outline": "#94a3b8",
                        "surface-container-high": "#bfdbfe",
                        "primary-container": "#1e3a8a",
                        "background": "#F3F4F6",
                        "on-surface-variant": "#475569",
                        "error": "#ba1a1a",
                        "primary": "#2563eb",
                        "surface-variant": "#dbeafe",
                        "on-secondary": "#ffffff",
                        "on-surface": "#1e293b",
                        "surface": "#f8faff",
                        "secondary-container": "#dbeafe",
                        "on-secondary-container": "#1e40af",
                        "inverse-surface": "#1e3a8a",
                        "inverse-primary": "#93c5fd",
                        "inverse-on-surface": "#eaf1ff",
                        "surface-container-low": "#f0f4ff",
                        "on-error": "#ffffff",
                        "secondary": "#6366f1",
                        "tertiary": "#93c5fd"
                    },
                    "fontFamily": {
                        "headline-lg": ["Inter"],
                        "headline-md": ["Inter"],
                        "body-md": ["Inter"],
                        "label-md": ["Inter"]
                    },
                    "fontSize": {
                        "headline-lg": ["32px", {"lineHeight": "1.2", "fontWeight": "700"}],
                        "headline-md": ["24px", {"lineHeight": "1.2", "fontWeight": "700"}],
                        "headline-sm": ["18px", {"lineHeight": "1.4", "fontWeight": "600"}],
                        "body-md": ["14px", {"lineHeight": "1.5", "fontWeight": "400"}],
                        "label-md": ["12px", {"lineHeight": "1.2", "fontWeight": "600"}]
                    },
                    "spacing": {
                        "container-padding": "1.5rem",
                        "inner-padding": "1rem"
                    }
                }
            }
        }
    </script>
    <style>
        .material-symbols-outlined { font-size: 20px; }
        .dropdown-menu { display: none; }
        .dropdown-menu:not(.hidden) { display: block; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(-4px); } to { opacity: 1; transform: translateY(0); } }
        .dropdown-menu:not(.hidden) { animation: fadeIn 0.15s ease; }
        
        /* Custom scrollbar matching the styled theme */
        .custom-scrollbar {
            scrollbar-width: thin;
            scrollbar-color: #64748b transparent;
        }
        .custom-scrollbar::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
            background: transparent;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
            background-color: #64748b;
            border-radius: 3px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
            background-color: #475569;
        }
        
        button, a, select, input[type="checkbox"], input[type="radio"], .cursor-pointer {
            cursor: pointer;
        }
        
        button.bg-gradient-to-r:hover,
        a.bg-gradient-to-r:hover,
        div.bg-gradient-to-r:hover {
            background-image: linear-gradient(to right, #1d4ed8, #1d4ed8) !important;
        }
        
        main {
            overflow-y: auto;
            overflow-x: hidden;
            scrollbar-width: thin;
            scrollbar-color: #64748b #f1f5f9;
        }
        main::-webkit-scrollbar {
            width: 7px;
        }
        main::-webkit-scrollbar-track {
            background: #f1f5f9;
        }
        main::-webkit-scrollbar-thumb {
            background-color: #64748b;
            border-radius: 4px;
        }
        main::-webkit-scrollbar-thumb:hover {
            background-color: #475569;
        }

        /* KANBAN GRID LAYOUT */
        #kanban-view {
            flex: 1 1 0;
            min-height: 0;
            display: flex;
            flex-direction: column;
            overflow-x: auto;
            overflow-y: hidden;
            scrollbar-width: auto;
            scrollbar-color: #64748b #f1f5f9;
        }
        #kanban-view::-webkit-scrollbar {
            height: 8px;
        }
        #kanban-view::-webkit-scrollbar-track {
            background: #f1f5f9;
            border-radius: 4px;
        }
        #kanban-view::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 4px;
        }
        #kanban-view::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }
        #kanban-inner-row {
            display: flex;
            gap: 1rem;
            padding: 1.5rem;
            height: 100%;
            min-width: max-content;
        }
        .kanban-column {
            width: 320px;
            flex-shrink: 0;
            display: flex;
            flex-direction: column;
            height: 100%;
        }
        .kanban-cards-container {
            overflow-y: auto;
            overflow-x: hidden;
            flex: 1 1 0%;
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
            padding: 0.5rem;
        }
        .kanban-subheader {
            display: flex;
            align-items: center;
            padding: 0.5rem 0.75rem;
            font-size: 0.75rem;
            border-bottom: 1px solid #e2e8f0;
            margin-bottom: 0.5rem;
        }
        .kanban-subheader.green {
            background-color: #ECFDF5;
            color: #0F766E;
            border-color: #A7F3D0;
        }
        .kanban-subheader.red {
            background-color: #FEE2E2;
            color: #991B1B;
            border-color: #FCA5A5;
        }
        .kanban-card {
            transition: opacity 0.2s, transform 0.15s, box-shadow 0.15s;
        }
        .kanban-card.dragging {
            opacity: 0.45;
            transform: scale(0.97);
            box-shadow: 0 8px 24px rgba(0,0,0,0.18) !important;
        }
        .kanban-cards-container.drag-over {
            background: rgba(37, 99, 235, 0.04);
            border-radius: 10px;
            outline: 2px dashed #2563EB;
            outline-offset: -3px;
        }
        .kanban-placeholder-card {
            border: 2px dashed #cbd5e1;
            border-radius: 0.75rem;
            padding: 2rem;
            text-align: center;
            color: #94a3b8;
            font-size: 0.875rem;
            font-weight: 500;
        }
        
        .hide-scrollbar::-webkit-scrollbar { display: none !important; }
        .hide-scrollbar { -ms-overflow-style: none !important; scrollbar-width: none !important; }
        
        .chevron-header {
            transition: all 0.2s ease-in-out;
            cursor: pointer;
        }
        .chevron-header:hover {
            filter: brightness(0.95);
        }
        .chevron-header.active-pink {
            background-color: #FEE2E2 !important;
            background-image: none !important;
            color: #991B1B !important;
        }
        .chevron-header.active-pink span {
            color: #991B1B !important;
        }
        .chevron-header.active-pink div {
            background-color: rgba(153, 27, 27, 0.1) !important;
            color: #991B1B !important;
        }
    </style>
</head>
<body class="bg-background text-on-surface font-body-md overflow-hidden flex h-screen">

<!-- Sidebar -->
<aside class="hidden md:flex flex-col h-screen py-inner-padding bg-gradient-to-b from-primary to-tertiary w-64 border-none shadow-2xl shrink-0">
    <div class="px-container-padding mb-8">
        <h1 class="text-headline-sm font-headline-sm font-black text-white">LEADS</h1>
        <p class="text-label-md font-label-md text-white/80">CRM ADMIN</p>
    </div>
    <nav class="flex-1 px-4 space-y-1">
        <a class="flex items-center px-4 py-3 bg-white/20 text-white backdrop-blur-md shadow-lg border border-white/20 rounded-xl font-bold" href="code.html">
            <span class="material-symbols-outlined mr-3">filter_list</span>
            <span class="text-label-md font-label-md">Leads</span>
        </a>
        <!-- Sub-items under Leads -->
        <div class="pl-4 space-y-0.5">
            <a class="flex items-center gap-2 px-4 py-2 bg-blue-100 text-[#2563EB] rounded-xl text-[12px] font-bold" href="code.html">
                <span class="material-symbols-outlined text-[16px]">grid_view</span>
                <span>Grid View</span>
            </a>
            <a class="flex items-center gap-2 px-4 py-2 text-[#2563EB] hover:bg-blue-50 transition-all rounded-xl text-[12px] font-semibold" href="listview.html">
                <span class="material-symbols-outlined text-[16px]">table_rows</span>
                <span>List View</span>
            </a>
        </div>
        <a class="flex items-center px-4 py-3 text-white/80 hover:bg-white/20 hover:text-white transition-all rounded-xl" href="settings.html">
            <span class="material-symbols-outlined mr-3">settings</span>
            <span class="text-label-md font-label-md">Settings</span>
        </a>
    </nav>
    <div class="mt-auto px-4 space-y-3 border-t border-white/20 pt-5 pb-2">
        <a class="flex items-center px-4 py-3 bg-white/10 hover:bg-white text-white hover:text-[#2563EB] rounded-2xl shadow-lg border border-white/30 hover:border-white hover:-translate-y-1 hover:shadow-2xl hover:shadow-black/20 transition-all duration-300 group backdrop-blur-md" href="#">
            <span class="material-symbols-outlined mr-3 text-[20px] group-hover:scale-110 transition-transform">help</span>
            <span class="text-[13px] font-bold tracking-wider">Help</span>
        </a>
        <a class="flex items-center px-4 py-3 bg-white/10 hover:bg-white text-white hover:text-[#2563EB] rounded-2xl shadow-lg border border-white/30 hover:border-white hover:-translate-y-1 hover:shadow-2xl hover:shadow-black/20 transition-all duration-300 group backdrop-blur-md" href="signin.html">
            <span class="material-symbols-outlined mr-3 text-[20px] group-hover:scale-110 transition-transform">logout</span>
            <span class="text-[13px] font-bold tracking-wider">Logout</span>
        </a>
    </div>
</aside>

<!-- Main Content -->
<main class="flex-1 flex flex-col min-w-0 overflow-y-auto overflow-x-hidden">

    <!-- Top Header -->
    <header class="flex justify-between items-center w-full px-container-padding h-12 bg-white border-b border-outline-variant z-10 shrink-0">
        <div class="flex items-center gap-2">
            <a href="code.html" class="text-slate-600 hover:text-slate-900 transition-colors flex items-center">
                <span class="material-symbols-outlined text-[20px] font-bold">arrow_back</span>
            </a>
            <h2 class="text-sm font-black text-slate-800 tracking-wide">LEADS</h2>
        </div>
        <div class="flex items-center gap-3">
            <!-- Live Clock -->
            <div id="clock-container" class="flex items-center gap-1.5 px-3 py-1 bg-slate-50 border border-slate-200 rounded-xl text-xs font-bold text-slate-600 shadow-sm whitespace-nowrap">
                <span class="material-symbols-outlined text-[15px] text-[#2563EB]">schedule</span>
                <span id="live-clock">--:--:--</span>
            </div>
            
            <!-- Fullscreen Button -->
            <button onclick="toggleFullscreen(this)" class="p-2 rounded-full hover:bg-slate-100 transition-colors flex items-center justify-center text-slate-600" title="Toggle Fullscreen">
                <span class="material-symbols-outlined text-[20px]">fullscreen</span>
            </button>
            
            <div class="text-[11px] font-bold text-slate-400">
                CRM &nbsp;&gt;&nbsp; <span class="text-slate-600">Leads / Grid View</span>
            </div>
        </div>
    </header>

    <!-- Toolbar -->
    <section class="flex items-center justify-between gap-3 px-container-padding py-2.5 bg-surface border-b border-outline-variant shrink-0 flex-wrap">
        <!-- Left: Controls -->
        <div class="flex items-center gap-2 flex-wrap">

            <!-- View Toggle -->
            <div class="relative">
                <button onclick="toggleDropdown(event, 'view-dropdown')" class="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-primary to-tertiary text-white border-none shadow-md rounded-full text-xs font-bold hover:from-[#1d4ed8] hover:to-[#1d4ed8] transition-all shadow-sm">
                    <span id="active-view-label">Grid View</span>
                    <span class="material-symbols-outlined text-[14px]">expand_more</span>
                </button>
                <div id="view-dropdown" class="absolute left-0 mt-1.5 w-36 bg-white border border-slate-100 rounded-xl shadow-lg py-1 z-20 hidden dropdown-menu">
                    <button onclick="setViewMode('grid')" class="w-full text-left px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors flex items-center justify-between">
                        Grid View <span id="grid-check" class="material-symbols-outlined text-[16px] text-[#2563EB]">check</span>
                    </button>
                    <a href="listview.html" class="w-full text-left px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors flex items-center justify-between">
                        List View <span class="material-symbols-outlined text-[16px] text-slate-300">open_in_new</span>
                    </a>
                </div>
            </div>

            <!-- Bulk Action (Hidden in Grid Mode by JS) -->
            <div id="bulk-action-container" class="flex flex-col hidden">
                <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-0.5">Bulk Action</span>
                <select id="bulk-action-select" onchange="handleBulkAction(this.value)" class="px-3 py-1.5 bg-white border border-slate-200 rounded-xl text-xs font-bold text-slate-700 min-w-[145px] focus:ring-2 focus:ring-primary focus:outline-none">
                    <option value="">Please Select</option>
                    <option value="delete">Delete Selected</option>
                    <option value="stage-lead">Change Stage: LEAD</option>
                    <option value="stage-followup">Change Stage: FOLLOW UP</option>
                    <option value="stage-onboarded">Change Stage: ONBOARDED</option>
                </select>
            </div>

            <!-- Customize Table (Hidden in Grid Mode by JS) -->
            <div id="customize-table-container" class="flex flex-col relative hidden">
                <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-0.5">Customize table</span>
                <button onclick="toggleDropdown(event, 'customize-dropdown')" class="flex items-center justify-between gap-2 px-3 py-1.5 bg-white border border-slate-200 rounded-xl text-xs font-bold text-slate-700 min-w-[145px] focus:ring-2 focus:ring-primary focus:outline-none shadow-sm">
                    <span id="customize-label">8 items selected</span>
                    <span class="material-symbols-outlined text-[14px]">expand_more</span>
                </button>
                <div id="customize-dropdown" class="absolute left-0 top-14 w-48 bg-white border border-slate-100 rounded-xl shadow-lg py-2 px-3 z-20 hidden dropdown-menu flex flex-col gap-1.5 text-xs font-semibold text-slate-700" onclick="event.stopPropagation()">
                    <label class="flex items-center gap-2 cursor-pointer py-1 hover:bg-slate-50 rounded px-1.5"><input type="checkbox" checked value="col-creation" onchange="toggleTableColumn(this)" class="rounded text-primary focus:ring-primary"> Creation Date</label>
                    <label class="flex items-center gap-2 cursor-pointer py-1 hover:bg-slate-50 rounded px-1.5"><input type="checkbox" checked value="col-modified" onchange="toggleTableColumn(this)" class="rounded text-primary focus:ring-primary"> Modified Date</label>
                    <label class="flex items-center gap-2 cursor-pointer py-1 hover:bg-slate-50 rounded px-1.5"><input type="checkbox" checked value="col-name" onchange="toggleTableColumn(this)" class="rounded text-primary focus:ring-primary"> Name</label>
                    <label class="flex items-center gap-2 cursor-pointer py-1 hover:bg-slate-50 rounded px-1.5"><input type="checkbox" checked value="col-mobile" onchange="toggleTableColumn(this)" class="rounded text-primary focus:ring-primary"> Mobile</label>
                    <label class="flex items-center gap-2 cursor-pointer py-1 hover:bg-slate-50 rounded px-1.5"><input type="checkbox" checked value="col-email" onchange="toggleTableColumn(this)" class="rounded text-primary focus:ring-primary"> Email</label>
                    <label class="flex items-center gap-2 cursor-pointer py-1 hover:bg-slate-50 rounded px-1.5"><input type="checkbox" checked value="col-user" onchange="toggleTableColumn(this)" class="rounded text-primary focus:ring-primary"> User</label>
                    <label class="flex items-center gap-2 cursor-pointer py-1 hover:bg-slate-50 rounded px-1.5"><input type="checkbox" checked value="col-source" onchange="toggleTableColumn(this)" class="rounded text-primary focus:ring-primary"> Source</label>
                    <label class="flex items-center gap-2 cursor-pointer py-1 hover:bg-slate-50 rounded px-1.5"><input type="checkbox" checked value="col-status" onchange="toggleTableColumn(this)" class="rounded text-primary focus:ring-primary"> Status</label>
                </div>
            </div>

            <!-- Status Dropdown (Shown in Grid Mode) -->
            <div id="status-dropdown-container" class="relative">
                <button onclick="toggleDropdown(event, 'status-dropdown')" class="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-primary to-tertiary text-white border-none shadow-md rounded-full text-xs font-bold hover:from-[#1d4ed8] hover:to-[#1d4ed8] transition-all shadow-sm">
                    <span id="active-status-label">Status: All</span>
                    <span class="material-symbols-outlined text-[14px]">expand_more</span>
                </button>
                <div id="status-dropdown" class="absolute left-0 mt-1.5 w-48 bg-white border border-slate-100 rounded-xl shadow-lg py-1 z-20 hidden dropdown-menu">
                    <button onclick="setStatusFilter('All')" class="w-full text-left px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors flex items-center justify-between">All <span id="status-All-check" class="material-symbols-outlined text-[16px] text-[#2563EB]">check</span></button>
                    <button onclick="setStatusFilter('LEAD')" class="w-full text-left px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors flex items-center justify-between">LEAD <span id="status-LEAD-check" class="material-symbols-outlined text-[16px] text-[#2563EB] hidden">check</span></button>
                    <button onclick="setStatusFilter('LOST')" class="w-full text-left px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors flex items-center justify-between">LOST <span id="status-LOST-check" class="material-symbols-outlined text-[16px] text-[#2563EB] hidden">check</span></button>
                    <button onclick="setStatusFilter('FOLLOW UP')" class="w-full text-left px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors flex items-center justify-between">FOLLOW UP <span id="status-FOLLOW UP-check" class="material-symbols-outlined text-[16px] text-[#2563EB] hidden">check</span></button>
                    <button onclick="setStatusFilter('PROPOSAL SENT')" class="w-full text-left px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors flex items-center justify-between">PROPOSAL SENT <span id="status-PROPOSAL SENT-check" class="material-symbols-outlined text-[16px] text-[#2563EB] hidden">check</span></button>
                    <button onclick="setStatusFilter('HOT')" class="w-full text-left px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors flex items-center justify-between">HOT <span id="status-HOT-check" class="material-symbols-outlined text-[16px] text-[#2563EB] hidden">check</span></button>
                    <button onclick="setStatusFilter('TRIAL AC')" class="w-full text-left px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors flex items-center justify-between">TRIAL AC <span id="status-TRIAL AC-check" class="material-symbols-outlined text-[16px] text-[#2563EB] hidden">check</span></button>
                    <button onclick="setStatusFilter('ONBOARDED')" class="w-full text-left px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors flex items-center justify-between">ONBOARDED <span id="status-ONBOARDED-check" class="material-symbols-outlined text-[16px] text-[#2563EB] hidden">check</span></button>
                    <button onclick="setStatusFilter('DEMO DONE')" class="w-full text-left px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors flex items-center justify-between">DEMO DONE <span id="status-DEMO DONE-check" class="material-symbols-outlined text-[16px] text-[#2563EB] hidden">check</span></button>
                </div>
            </div>

            <!-- Sort By (Shown in Grid Mode) -->
            <div id="sort-dropdown-container" class="relative">
                <button onclick="toggleDropdown(event, 'sort-dropdown')" class="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-primary to-tertiary text-white border-none shadow-md rounded-full text-xs font-bold hover:from-[#1d4ed8] hover:to-[#1d4ed8] transition-all shadow-sm">
                    <span id="active-sort-label">Created Date</span>
                    <span class="material-symbols-outlined text-[14px]">expand_more</span>
                </button>
                <div id="sort-dropdown" class="absolute left-0 mt-1.5 w-40 bg-white border border-slate-100 rounded-xl shadow-lg py-1 z-20 hidden dropdown-menu">
                    <button onclick="setSortField('date')" class="w-full text-left px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors flex items-center justify-between">Created Date <span id="sort-date-check" class="material-symbols-outlined text-[16px] text-[#2563EB]">check</span></button>
                    <button onclick="setSortField('modified')" class="w-full text-left px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors flex items-center justify-between">Modified Date <span id="sort-modified-check" class="material-symbols-outlined text-[16px] text-[#2563EB] hidden">check</span></button>
                    <button onclick="setSortField('amount')" class="w-full text-left px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors flex items-center justify-between">Deal Value <span id="sort-amount-check" class="material-symbols-outlined text-[16px] text-[#2563EB] hidden">check</span></button>
                    <button onclick="setSortField('source')" class="w-full text-left px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors flex items-center justify-between">Source <span id="sort-source-check" class="material-symbols-outlined text-[16px] text-[#2563EB] hidden">check</span></button>
                    <button onclick="setSortField('stage')" class="w-full text-left px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors flex items-center justify-between">Status <span id="sort-stage-check" class="material-symbols-outlined text-[16px] text-[#2563EB] hidden">check</span></button>
                    <button onclick="setSortField('score')" class="w-full text-left px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors flex items-center justify-between">Score <span id="sort-score-check" class="material-symbols-outlined text-[16px] text-[#2563EB] hidden">check</span></button>
                    <button onclick="setSortField('name')" class="w-full text-left px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors flex items-center justify-between">Name <span id="sort-name-check" class="material-symbols-outlined text-[16px] text-[#2563EB] hidden">check</span></button>
                </div>
            </div>

            <!-- Sort Order (Shown in Grid Mode) -->
            <div id="order-dropdown-container" class="relative">
                <button onclick="toggleDropdown(event, 'order-dropdown')" class="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-primary to-tertiary text-white border-none shadow-md rounded-full text-xs font-bold hover:from-[#1d4ed8] hover:to-[#1d4ed8] transition-all shadow-sm">
                    <span id="active-order-label">Descending</span>
                    <span class="material-symbols-outlined text-[14px]">expand_more</span>
                </button>
                <div id="order-dropdown" class="absolute left-0 mt-1.5 w-36 bg-white border border-slate-100 rounded-xl shadow-lg py-1 z-20 hidden dropdown-menu">
                    <button onclick="setSortOrder('desc')" class="w-full text-left px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors flex items-center justify-between">Descending <span id="order-desc-check" class="material-symbols-outlined text-[16px] text-[#2563EB]">check</span></button>
                    <button onclick="setSortOrder('asc')" class="w-full text-left px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors flex items-center justify-between">Ascending <span id="order-asc-check" class="material-symbols-outlined text-[16px] text-[#2563EB] hidden">check</span></button>
                </div>
            </div>

        </div>

        <!-- Right: Search & Action Buttons -->
        <div class="flex items-center gap-2 shrink-0">
            <div class="relative w-48">
                <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant text-[18px]">search</span>
                <input id="search-leads-input" oninput="handleSearchLeads(this.value)" class="w-full pl-9 pr-3 py-1.5 rounded-xl border border-outline-variant bg-surface-container-lowest focus:ring-2 focus:ring-primary focus:outline-none text-sm" placeholder="Search leads..." type="text"/>
            </div>
            <button class="px-4 py-2 bg-gradient-to-r from-primary to-tertiary text-white border-none hover:from-[#1d4ed8] hover:to-[#1d4ed8] text-white rounded-xl text-xs font-bold transition-all shadow-sm whitespace-nowrap">Integration</button>
            <button class="px-4 py-2 bg-gradient-to-r from-primary to-tertiary text-white border-none hover:from-[#1d4ed8] hover:to-[#1d4ed8] text-white rounded-xl text-xs font-bold transition-all shadow-sm whitespace-nowrap">Import</button>
            <button class="px-4 py-2 bg-gradient-to-r from-primary to-tertiary text-white border-none hover:from-[#1d4ed8] hover:to-[#1d4ed8] text-white rounded-xl text-xs font-bold transition-all shadow-sm whitespace-nowrap">Import History</button>
            <button onclick="openAddLeadModal()" class="flex items-center gap-1.5 px-5 py-2 bg-gradient-to-r from-primary to-tertiary text-white border-none hover:from-[#1d4ed8] hover:to-[#1d4ed8] text-white rounded-xl text-xs font-bold transition-all shadow-sm whitespace-nowrap">
                <span class="material-symbols-outlined text-[16px]">add</span> Add Lead
            </button>
            <button onclick="handleRefreshLeads()" class="p-2 bg-[#2563eb] hover:bg-[#1d4ed8] text-white border-none rounded-full transition-all shadow-sm flex items-center justify-center">
                <span class="material-symbols-outlined text-[16px]">refresh</span>
            </button>
        </div>
    </section>

    <!-- Content Scroller Container -->
    <div id="content-view-container" class="flex-1 overflow-hidden flex flex-col relative">

        <!-- 1. KANBAN GRID VIEW -->
        <div id="kanban-view" class="flex-1 overflow-x-auto overflow-y-hidden bg-[#F8FAFC]">
            <div id="kanban-inner-row">
                
                <!-- 1. LEAD -->
                <div class="kanban-column flex-shrink-0 w-80 bg-slate-100/40 border border-slate-200 rounded-2xl flex flex-col h-full min-h-0">
                    <header class="chevron-header bg-[#ECFDF5] border-b border-emerald-100/80 px-4 py-2.5 flex items-center gap-2 select-none rounded-t-2xl">
                        <div class="w-5 h-5 rounded-full bg-white flex items-center justify-center shrink-0 shadow-sm">
                            <span class="material-symbols-outlined text-[13px] text-[#0F172A] font-bold">info</span>
                        </div>
                        <span class="text-xs font-bold tracking-wide uppercase flex-1 text-[#0F172A]">LEAD</span>
                        <span onclick="event.stopPropagation(); openAddLeadModal()" class="material-symbols-outlined text-[16px] cursor-pointer hover:bg-emerald-100 rounded p-0.5 text-[#0F172A]">add</span>
                    </header>
                    <div class="kanban-subheader green" data-subheader></div>
                    <div class="kanban-cards-container custom-scrollbar" data-stage="LEAD"></div>
                </div>

                <!-- 2. LOST -->
                <div class="kanban-column flex-shrink-0 w-80 bg-slate-100/40 border border-slate-200 rounded-2xl flex flex-col h-full min-h-0">
                    <header class="chevron-header bg-[#ECFDF5] border-b border-emerald-100/80 px-4 py-2.5 flex items-center gap-2 select-none rounded-t-2xl">
                        <div class="w-5 h-5 rounded-full bg-white flex items-center justify-center shrink-0 shadow-sm">
                            <span class="material-symbols-outlined text-[13px] text-[#0F172A] font-bold">cancel</span>
                        </div>
                        <span class="text-xs font-bold tracking-wide uppercase flex-1 text-[#0F172A]">LOST</span>
                        <span onclick="event.stopPropagation(); openAddLeadModal()" class="material-symbols-outlined text-[16px] cursor-pointer hover:bg-emerald-100 rounded p-0.5 text-[#0F172A]">add</span>
                    </header>
                    <div class="kanban-subheader green" data-subheader></div>
                    <div class="kanban-cards-container custom-scrollbar" data-stage="LOST"></div>
                </div>

                <!-- 3. FOLLOW UP -->
                <div class="kanban-column flex-shrink-0 w-80 bg-slate-100/40 border border-slate-200 rounded-2xl flex flex-col h-full min-h-0">
                    <header class="chevron-header bg-[#ECFDF5] border-b border-emerald-100/80 px-4 py-2.5 flex items-center gap-2 select-none rounded-t-2xl">
                        <div class="w-5 h-5 rounded-full bg-white flex items-center justify-center shrink-0 shadow-sm">
                            <span class="material-symbols-outlined text-[13px] text-[#0F172A] font-bold">repeat</span>
                        </div>
                        <span class="text-xs font-bold tracking-wide uppercase flex-1 text-[#0F172A]">FOLLOW UP</span>
                        <span onclick="event.stopPropagation(); openAddLeadModal()" class="material-symbols-outlined text-[16px] cursor-pointer hover:bg-emerald-100 rounded p-0.5 text-[#0F172A]">add</span>
                    </header>
                    <div class="kanban-subheader green" data-subheader></div>
                    <div class="kanban-cards-container custom-scrollbar" data-stage="FOLLOW UP"></div>
                </div>

                <!-- 4. PROPOSAL SENT -->
                <div class="kanban-column flex-shrink-0 w-80 bg-slate-100/40 border border-slate-200 rounded-2xl flex flex-col h-full min-h-0">
                    <header class="chevron-header bg-[#ECFDF5] border-b border-emerald-100/80 px-4 py-2.5 flex items-center gap-2 select-none rounded-t-2xl">
                        <div class="w-5 h-5 rounded-full bg-white flex items-center justify-center shrink-0 shadow-sm">
                            <span class="material-symbols-outlined text-[13px] text-[#0F172A] font-bold">description</span>
                        </div>
                        <span class="text-xs font-bold tracking-wide uppercase flex-1 text-[#0F172A]">PROPOSAL SENT</span>
                        <span onclick="event.stopPropagation(); openAddLeadModal()" class="material-symbols-outlined text-[16px] cursor-pointer hover:bg-emerald-100 rounded p-0.5 text-[#0F172A]">add</span>
                    </header>
                    <div class="kanban-subheader green" data-subheader></div>
                    <div class="kanban-cards-container custom-scrollbar" data-stage="PROPOSAL SENT"></div>
                </div>

                <!-- 5. OTHERS -->
                <div class="kanban-column flex-shrink-0 w-80 bg-slate-100/40 border border-slate-200 rounded-2xl flex flex-col h-full min-h-0">
                    <header class="chevron-header bg-[#ECFDF5] border-b border-emerald-100/80 px-4 py-2.5 flex items-center gap-2 select-none rounded-t-2xl">
                        <div class="w-5 h-5 rounded-full bg-white flex items-center justify-center shrink-0 shadow-sm">
                            <span class="material-symbols-outlined text-[13px] text-[#0F172A] font-bold">more_horiz</span>
                        </div>
                        <span class="text-xs font-bold tracking-wide uppercase flex-1 text-[#0F172A]">OTHERS</span>
                        <span onclick="event.stopPropagation(); openAddLeadModal()" class="material-symbols-outlined text-[16px] cursor-pointer hover:bg-emerald-100 rounded p-0.5 text-[#0F172A]">add</span>
                    </header>
                    <div class="kanban-subheader green" data-subheader></div>
                    <div class="kanban-cards-container custom-scrollbar" data-stage="OTHERS"></div>
                </div>

                <!-- 6. HOT -->
                <div class="kanban-column flex-shrink-0 w-80 bg-slate-100/40 border border-slate-200 rounded-2xl flex flex-col h-full min-h-0">
                    <header class="chevron-header bg-[#ECFDF5] border-b border-emerald-100/80 px-4 py-2.5 flex items-center gap-2 select-none rounded-t-2xl">
                        <div class="w-5 h-5 rounded-full bg-white flex items-center justify-center shrink-0 shadow-sm">
                            <span class="material-symbols-outlined text-[13px] text-[#0F172A] font-bold">local_fire_department</span>
                        </div>
                        <span class="text-xs font-bold tracking-wide uppercase flex-1 text-[#0F172A]">HOT</span>
                        <span onclick="event.stopPropagation(); openAddLeadModal()" class="material-symbols-outlined text-[16px] cursor-pointer hover:bg-emerald-100 rounded p-0.5 text-[#0F172A]">add</span>
                    </header>
                    <div class="kanban-subheader green" data-subheader></div>
                    <div class="kanban-cards-container custom-scrollbar" data-stage="HOT"></div>
                </div>

                <!-- 7. TRIAL AC -->
                <div class="kanban-column flex-shrink-0 w-80 bg-slate-100/40 border border-slate-200 rounded-2xl flex flex-col h-full min-h-0">
                    <header class="chevron-header bg-[#ECFDF5] border-b border-emerald-100/80 px-4 py-2.5 flex items-center gap-2 select-none rounded-t-2xl">
                        <div class="w-5 h-5 rounded-full bg-white flex items-center justify-center shrink-0 shadow-sm">
                            <span class="material-symbols-outlined text-[13px] text-[#0F172A] font-bold">science</span>
                        </div>
                        <span class="text-xs font-bold tracking-wide uppercase flex-1 text-[#0F172A]">TRIAL AC</span>
                        <span onclick="event.stopPropagation(); openAddLeadModal()" class="material-symbols-outlined text-[16px] cursor-pointer hover:bg-emerald-100 rounded p-0.5 text-[#0F172A]">add</span>
                    </header>
                    <div class="kanban-subheader green" data-subheader></div>
                    <div class="kanban-cards-container custom-scrollbar" data-stage="TRIAL AC"></div>
                </div>

                <!-- 8. ONBOARDED -->
                <div class="kanban-column flex-shrink-0 w-80 bg-slate-100/40 border border-slate-200 rounded-2xl flex flex-col h-full min-h-0">
                    <header class="chevron-header bg-[#ECFDF5] border-b border-emerald-100/80 px-4 py-2.5 flex items-center gap-2 select-none rounded-t-2xl">
                        <div class="w-5 h-5 rounded-full bg-white flex items-center justify-center shrink-0 shadow-sm">
                            <span class="material-symbols-outlined text-[13px] text-[#0F172A] font-bold">check_circle</span>
                        </div>
                        <span class="text-xs font-bold tracking-wide uppercase flex-1 text-[#0F172A]">ONBOARDED</span>
                        <span onclick="event.stopPropagation(); openAddLeadModal()" class="material-symbols-outlined text-[16px] cursor-pointer hover:bg-emerald-100 rounded p-0.5 text-[#0F172A]">add</span>
                    </header>
                    <div class="kanban-subheader green" data-subheader></div>
                    <div class="kanban-cards-container custom-scrollbar" data-stage="ONBOARDED"></div>
                </div>

                <!-- 9. DEMO DONE -->
                <div class="kanban-column flex-shrink-0 w-80 bg-slate-100/40 border border-slate-200 rounded-2xl flex flex-col h-full min-h-0">
                    <header class="chevron-header bg-[#ECFDF5] border-b border-emerald-100/80 px-4 py-2.5 flex items-center gap-2 select-none rounded-t-2xl">
                        <div class="w-5 h-5 rounded-full bg-white flex items-center justify-center shrink-0 shadow-sm">
                            <span class="material-symbols-outlined text-[13px] text-[#0F172A] font-bold">slideshow</span>
                        </div>
                        <span class="text-xs font-bold tracking-wide uppercase flex-1 text-[#0F172A]">DEMO DONE</span>
                        <span onclick="event.stopPropagation(); openAddLeadModal()" class="material-symbols-outlined text-[16px] cursor-pointer hover:bg-emerald-100 rounded p-0.5 text-[#0F172A]">add</span>
                    </header>
                    <div class="kanban-subheader green" data-subheader></div>
                    <div class="kanban-cards-container custom-scrollbar" data-stage="DEMO DONE"></div>
                </div>

                <!-- 10. RNR -->
                <div class="kanban-column flex-shrink-0 w-80 bg-slate-100/40 border border-slate-200 rounded-2xl flex flex-col h-full min-h-0">
                    <header class="chevron-header bg-[#ECFDF5] border-b border-emerald-100/80 px-4 py-2.5 flex items-center gap-2 select-none rounded-t-2xl">
                        <div class="w-5 h-5 rounded-full bg-white flex items-center justify-center shrink-0 shadow-sm">
                            <span class="material-symbols-outlined text-[13px] text-[#0F172A] font-bold">phone_disabled</span>
                        </div>
                        <span class="text-xs font-bold tracking-wide uppercase flex-1 text-[#0F172A]">RNR</span>
                        <span onclick="event.stopPropagation(); openAddLeadModal()" class="material-symbols-outlined text-[16px] cursor-pointer hover:bg-emerald-100 rounded p-0.5 text-[#0F172A]">add</span>
                    </header>
                    <div class="kanban-subheader green" data-subheader></div>
                    <div class="kanban-cards-container custom-scrollbar" data-stage="RNR"></div>
                </div>

                <!-- 11. CALL BACK -->
                <div class="kanban-column flex-shrink-0 w-80 bg-slate-100/40 border border-slate-200 rounded-2xl flex flex-col h-full min-h-0">
                    <header class="chevron-header bg-[#ECFDF5] border-b border-emerald-100/80 px-4 py-2.5 flex items-center gap-2 select-none rounded-t-2xl">
                        <div class="w-5 h-5 rounded-full bg-white flex items-center justify-center shrink-0 shadow-sm">
                            <span class="material-symbols-outlined text-[13px] text-[#0F172A] font-bold">phone_callback</span>
                        </div>
                        <span class="text-xs font-bold tracking-wide uppercase flex-1 text-[#0F172A]">CALL BACK</span>
                        <span onclick="event.stopPropagation(); openAddLeadModal()" class="material-symbols-outlined text-[16px] cursor-pointer hover:bg-emerald-100 rounded p-0.5 text-[#0F172A]">add</span>
                    </header>
                    <div class="kanban-subheader green" data-subheader></div>
                    <div class="kanban-cards-container custom-scrollbar" data-stage="CALL BACK"></div>
                </div>

                <!-- 12. INVOICE -->
                <div class="kanban-column flex-shrink-0 w-80 bg-slate-100/40 border border-slate-200 rounded-2xl flex flex-col h-full min-h-0">
                    <header class="chevron-header bg-[#ECFDF5] border-b border-emerald-100/80 px-4 py-2.5 flex items-center gap-2 select-none rounded-t-2xl">
                        <div class="w-5 h-5 rounded-full bg-white flex items-center justify-center shrink-0 shadow-sm">
                            <span class="material-symbols-outlined text-[13px] text-[#0F172A] font-bold">receipt_long</span>
                        </div>
                        <span class="text-xs font-bold tracking-wide uppercase flex-1 text-[#0F172A]">INVOICE</span>
                        <span onclick="event.stopPropagation(); openAddLeadModal()" class="material-symbols-outlined text-[16px] cursor-pointer hover:bg-emerald-100 rounded p-0.5 text-[#0F172A]">add</span>
                    </header>
                    <div class="kanban-subheader green" data-subheader></div>
                    <div class="kanban-cards-container custom-scrollbar" data-stage="INVOICE"></div>
                </div>

                <!-- 13. DEMO SCHEDULE -->
                <div class="kanban-column flex-shrink-0 w-80 bg-slate-100/40 border border-slate-200 rounded-2xl flex flex-col h-full min-h-0">
                    <header class="chevron-header bg-[#ECFDF5] border-b border-emerald-100/80 px-4 py-2.5 flex items-center gap-2 select-none rounded-t-2xl">
                        <div class="w-5 h-5 rounded-full bg-white flex items-center justify-center shrink-0 shadow-sm">
                            <span class="material-symbols-outlined text-[13px] text-[#0F172A] font-bold">event</span>
                        </div>
                        <span class="text-xs font-bold tracking-wide uppercase flex-1 text-[#0F172A]">DEMO SCHEDULE</span>
                        <span onclick="event.stopPropagation(); openAddLeadModal()" class="material-symbols-outlined text-[16px] cursor-pointer hover:bg-emerald-100 rounded p-0.5 text-[#0F172A]">add</span>
                    </header>
                    <div class="kanban-subheader green" data-subheader></div>
                    <div class="kanban-cards-container custom-scrollbar" data-stage="DEMO SCHEDULE"></div>
                </div>

            </div>
        </div>

        <!-- 2. TABLE LIST VIEW (RENDERED FROM JS AS VIEWMODE SWITCH) -->
        <div id="table-view" class="hidden flex-1 p-6 overflow-y-auto custom-scrollbar">
            <div class="bg-white border border-outline-variant rounded-2xl shadow-sm overflow-hidden">
                <div class="overflow-x-auto w-full">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="bg-gradient-to-r from-primary to-tertiary border-none shadow-md text-[11px] font-bold text-white uppercase tracking-wider">
                                <th class="py-3 px-4 w-12 text-center">
                                    <input type="checkbox" id="select-all-leads" onchange="toggleSelectAll(this)" class="rounded border-slate-300 w-4 h-4 cursor-pointer">
                                </th>
                                <th class="py-3 px-6 w-12 text-center">Sr.</th>
                                <th class="py-3 px-6 col-creation">Creation Date</th>
                                <th class="py-3 px-6 col-modified">Modified Date</th>
                                <th class="py-3 px-6 col-name">Name</th>
                                <th class="py-3 px-6 col-mobile">Mobile</th>
                                <th class="py-3 px-6 col-email">Email</th>
                                <th class="py-3 px-6 col-user">User</th>
                                <th class="py-3 px-6 col-source">Source</th>
                                <th class="py-3 px-6 col-status">Status</th>
                                <th class="py-3 px-6 text-right">Action</th>
                            </tr>
                        </thead>
                        <tbody id="leads-table-body" class="divide-y divide-slate-100 text-xs font-semibold text-slate-700">
                            <!-- Rendered dynamically -->
                        </tbody>
                    </table>
                </div>
                <!-- Footer: total count -->
                <div class="px-6 py-3 border-t border-slate-100 flex items-center justify-between">
                    <span id="record-count" class="text-[11px] font-semibold text-slate-400">0 records</span>
                </div>
            </div>
        </div>

        <!-- Scroll to Top (only visible when table-view is scrolled) -->
        <button onclick="scrollToTop()" class="fixed bottom-6 right-6 w-10 h-10 rounded-xl bg-gradient-to-r from-primary to-tertiary text-white border-none hover:from-[#1d4ed8] hover:to-[#1d4ed8] text-white transition-all shadow-md flex items-center justify-center hover:scale-105 active:scale-95 z-30">
            <span class="material-symbols-outlined text-[20px] font-bold">arrow_upward</span>
        </button>

    </div>

</main>

<!-- Add/Edit Lead Modal -->
<div id="lead-modal" class="hidden fixed inset-0 bg-black/40 z-50 flex items-center justify-center p-4 animate-fade-in">
    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg">
        <header class="flex justify-between items-center px-6 pt-5 pb-3 border-b border-slate-100">
            <h3 id="modal-title" class="text-sm font-black text-slate-800">Add New Lead</h3>
            <button onclick="closeLeadModal()" class="text-slate-400 hover:text-slate-700 transition-colors">
                <span class="material-symbols-outlined">close</span>
            </button>
        </header>
        <form id="lead-form" onsubmit="handleLeadSubmit(event)" class="px-6 py-4 flex flex-col gap-3">
            <input type="hidden" id="edit-lead-original-name"/>
            <div class="grid grid-cols-2 gap-3">
                <div class="flex flex-col gap-1 col-span-2">
                    <label for="lead-name" class="text-slate-500 uppercase tracking-wider text-[10px]">Company / Name *</label>
                    <input type="text" id="lead-name" required placeholder="e.g. Acme Corp" class="px-3 py-2 bg-[#F3F4F6] border border-slate-200 rounded-xl focus:ring-2 focus:ring-primary focus:outline-none text-slate-800 text-sm">
                </div>
                <div class="flex flex-col gap-1">
                    <label for="lead-email" class="text-slate-500 uppercase tracking-wider text-[10px]">Email</label>
                    <input type="email" id="lead-email" placeholder="email@example.com" class="px-3 py-2 bg-[#F3F4F6] border border-slate-200 rounded-xl focus:ring-2 focus:ring-primary focus:outline-none text-slate-800 text-sm">
                </div>
                <div class="flex flex-col gap-1">
                    <label for="lead-mobile" class="text-slate-500 uppercase tracking-wider text-[10px]">Mobile</label>
                    <input type="text" id="lead-mobile" placeholder="+1 000-000-0000" class="px-3 py-2 bg-[#F3F4F6] border border-slate-200 rounded-xl focus:ring-2 focus:ring-primary focus:outline-none text-slate-800 text-sm">
                </div>
                <div class="flex flex-col gap-1">
                    <label for="lead-stage" class="text-slate-500 uppercase tracking-wider text-[10px]">Stage</label>
                    <select id="lead-stage" class="px-3 py-2 bg-[#F3F4F6] border border-slate-200 rounded-xl focus:ring-2 focus:ring-primary focus:outline-none text-slate-800 text-sm">
                        <option value="LEAD">LEAD</option>
                        <option value="LOST">LOST</option>
                        <option value="FOLLOW UP">FOLLOW UP</option>
                        <option value="PROPOSAL SENT">PROPOSAL SENT</option>
                        <option value="HOT">HOT</option>
                        <option value="OTHERS">OTHERS</option>
                        <option value="TRIAL AC">TRIAL AC</option>
                        <option value="ONBOARDED">ONBOARDED</option>
                        <option value="DEMO DONE">DEMO DONE</option>
                        <option value="RNR">RNR</option>
                        <option value="CALL BACK">CALL BACK</option>
                        <option value="INVOICE">INVOICE</option>
                        <option value="DEMO SCHEDULE">DEMO SCHEDULE</option>
                    </select>
                </div>
                <div class="flex flex-col gap-1">
                    <label for="lead-source" class="text-slate-500 uppercase tracking-wider text-[10px]">Source</label>
                    <select id="lead-source" class="px-3 py-2 bg-[#F3F4F6] border border-slate-200 rounded-xl focus:ring-2 focus:ring-primary focus:outline-none text-slate-800 text-sm">
                        <option value="Direct Sales">Direct Sales</option>
                        <option value="Webinar">Webinar</option>
                        <option value="Google Ads">Google Ads</option>
                        <option value="Referral">Referral</option>
                        <option value="-">-</option>
                    </select>
                </div>
                <div class="flex flex-col gap-1">
                    <label for="lead-user" class="text-slate-500 uppercase tracking-wider text-[10px]">Assigned User</label>
                    <select id="lead-user" class="px-3 py-2 bg-[#F3F4F6] border border-slate-200 rounded-xl focus:ring-2 focus:ring-primary focus:outline-none text-slate-800 text-sm">
                        <option value="Mark Taylor">Mark Taylor</option>
                        <option value="John Doe">John Doe</option>
                        <option value="Sarah Smith">Sarah Smith</option>
                        <option value="-">-</option>
                    </select>
                </div>
                <div class="flex flex-col gap-1">
                    <label for="lead-amount" class="text-slate-550 uppercase tracking-wider text-[10px]">Amount</label>
                    <input type="text" id="lead-amount" placeholder="0" class="px-3 py-2 bg-[#F3F4F6] border border-slate-200 rounded-xl focus:ring-2 focus:ring-primary focus:outline-none text-slate-800 text-sm">
                </div>
                <div class="flex flex-col gap-1">
                    <label for="lead-status-field" class="text-slate-550 uppercase tracking-wider text-[10px]">Status</label>
                    <input type="text" id="lead-status-field" class="px-3 py-2 bg-[#F3F4F6] border border-slate-200 rounded-xl focus:ring-2 focus:ring-primary focus:outline-none text-slate-800 text-sm">
                </div>
                <div class="flex flex-col gap-1">
                    <label for="lead-priority" class="text-slate-550 uppercase tracking-wider text-[10px]">Priority</label>
                    <select id="lead-priority" class="px-3 py-2 bg-[#F3F4F6] border border-slate-200 rounded-xl focus:ring-2 focus:ring-primary focus:outline-none text-slate-800 text-sm">
                        <option value="Low">Low</option>
                        <option value="Medium">Medium</option>
                        <option value="High">High</option>
                    </select>
                </div>
                <div class="flex flex-col gap-1">
                    <label for="lead-completed-date" class="text-slate-550 uppercase tracking-wider text-[10px]">Completed Date</label>
                    <input type="text" id="lead-completed-date" placeholder="e.g. 21-May-2026" class="px-3 py-2 bg-[#F3F4F6] border border-slate-200 rounded-xl focus:ring-2 focus:ring-primary focus:outline-none text-slate-800 text-sm">
                </div>
                <div class="flex flex-col gap-1 col-span-2">
                    <label for="lead-creation-date" class="text-slate-550 uppercase tracking-wider text-[10px]">Creation Date</label>
                    <input type="text" id="lead-creation-date" placeholder="e.g. 21-May-2026 06:12 PM" class="px-3 py-2 bg-[#F3F4F6] border border-slate-200 rounded-xl focus:ring-2 focus:ring-primary focus:outline-none text-slate-800 text-sm">
                </div>
            </div>
            <footer class="mt-2 flex justify-end gap-2.5">
                <button type="button" onclick="closeLeadModal()" class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-xl transition-colors text-sm">Cancel</button>
                <button type="submit" class="px-5 py-2 bg-gradient-to-r from-primary to-tertiary text-white border-none hover:from-[#1d4ed8] hover:to-[#1d4ed8] text-white font-bold rounded-xl shadow-sm transition-colors text-sm">Save Lead</button>
            </footer>
        </form>
    </div>
</div>

<script>
// Live clock init function
function initClock() {
    const clockEl = document.getElementById('live-clock');
    if (!clockEl) return;
    const updateTime = () => {
        const now = new Date();
        clockEl.textContent = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true });
    };
    updateTime();
    setInterval(updateTime, 1000);
}

// Fullscreen toggle function
function toggleFullscreen(btn) {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(err => {
            console.error(`Error attempting to enable fullscreen: ${err.message}`);
        });
        if (btn && btn.firstElementChild) {
            btn.firstElementChild.textContent = 'fullscreen_exit';
        }
    } else {
        document.exitFullscreen();
        if (btn && btn.firstElementChild) {
            btn.firstElementChild.textContent = 'fullscreen';
        }
    }
}

""" + js_content + """
</script>
</body>
</html>
"""

# Write to code.html
with open(code_html_path, "w", encoding="utf-8", newline="\r\n") as f:
    f.write(html_content)

print("Assembly of code.html finished successfully!")
