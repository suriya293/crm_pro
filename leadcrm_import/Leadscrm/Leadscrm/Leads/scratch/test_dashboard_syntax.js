

        tailwind.config = { darkMode: "class" }

    // Fullscreen Toggle
    function toggleFullscreen(button) {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen().catch(err => {
                alert(`Error attempting to enable full-screen mode: ${err.message}`);
            });
        } else {
            document.exitFullscreen();
        }
    }

    // Live Clock
    function initClock() {
        const clock = document.getElementById('live-clock');
        const update = () => {
            const now = new Date();
            const dd = String(now.getDate()).padStart(2, '0');
            const mm = String(now.getMonth()+1).padStart(2, '0');
            const yyyy = now.getFullYear();
            const hh = String(now.getHours()).padStart(2, '0');
            const min = String(now.getMinutes()).padStart(2, '0');
            const ss = String(now.getSeconds()).padStart(2, '0');
            if (clock) clock.textContent = `${dd}-${mm}-${yyyy} ${hh}:${min}:${ss}`;
        };
        update();
        setInterval(update, 1000);
    }

    // Admin Dropdown Toggle
    function toggleAdminMenu(event) {
        event.stopPropagation();
        const menu = document.getElementById('admin-menu');
        if (menu) menu.classList.toggle('hidden');
    }
    document.addEventListener('click', () => {
        const menu = document.getElementById('admin-menu');
        if (menu) menu.classList.add('hidden');
    });

    // Dark Mode Toggle
    function initDarkMode() {
        if (localStorage.getItem('darkMode') === 'enabled') {
            document.documentElement.classList.add('dark');
        }
    }
    function toggleDarkMode() {
        if (document.documentElement.classList.contains('dark')) {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('darkMode', 'disabled');
        } else {
            document.documentElement.classList.add('dark');
            localStorage.setItem('darkMode', 'enabled');
        }
    }

    // Date filter state
    let currentFilter = 'all';
    let currentSourceFilter = 'all';
    let currentStageFilter = 'all';

    function toggleDateDropdown(event) {
        event.stopPropagation();
        const menu = document.getElementById('date-filter-dropdown');
        if (menu) menu.classList.toggle('hidden');
    }

    function selectDateFilter(filterVal, label) {
        currentFilter = filterVal;
        const displayLabel = document.getElementById('selected-date-filter');
        if (displayLabel) displayLabel.textContent = label;
        loadStats();
    }

    function toggleConversionsDownloadDropdown(event) {
        event.stopPropagation();
        const menu = document.getElementById('conversions-download-dropdown-menu');
        if (menu) menu.classList.toggle('hidden');
    }

    function selectStageFilter(filterVal) {
        currentStageFilter = filterVal;
        
        // Update UI buttons
        const filters = ['today', '1week', '15days', '1month', 'all'];
        filters.forEach(f => {
            const btn = document.getElementById(`btn-stage-filter-${f}`);
            if (btn) {
                if (f === filterVal) {
                    btn.className = "px-2.5 py-1 rounded-lg transition-all text-slate-700 dark:text-slate-300 bg-white dark:bg-slate-700 shadow-sm";
                } else {
                    btn.className = "px-2.5 py-1 rounded-lg transition-all text-slate-500 hover:text-slate-800 dark:text-slate-400 dark:hover:text-slate-200 bg-transparent";
                }
            }
        });
        
        loadStats();
    }

    function toggleSourceDateDropdown(event) {
        event.stopPropagation();
        const menu = document.getElementById('source-date-filter-dropdown');
        if (menu) menu.classList.toggle('hidden');
    }

    function selectSourceDateFilter(filterVal, label) {
        currentSourceFilter = filterVal;
        const displayLabel = document.getElementById('selected-source-date-filter');
        if (displayLabel) displayLabel.textContent = label;
        loadStats();
    }

    document.addEventListener('click', () => {
        const cpMenu = document.getElementById('conversions-download-dropdown-menu');
        if (cpMenu) cpMenu.classList.add('hidden');
        const menu = document.getElementById('date-filter-dropdown');
        if (menu) menu.classList.add('hidden');
        const srcMenu = document.getElementById('source-date-filter-dropdown');
        if (srcMenu) srcMenu.classList.add('hidden');
    });

    function getSVGStatusGradientId(statusName) {
        const s = statusName.toUpperCase();
        if (s.includes("HOT")) return "grad-hot";
        if (s.includes("LOST") || s.includes("DUPLICATE")) return "grad-slate";
        if (s.includes("ONBOARDED")) return "grad-onboarded";
        if (s.includes("PROPOSAL")) return "grad-proposal";
        if (s.includes("DEMO SCHEDULED") || s.includes("DEMO SCHEDULE")) return "grad-demo-scheduled";
        if (s.includes("DEMO DONE") || s.includes("DEMO")) return "grad-demo-done";
        if (s.includes("INVOICE")) return "grad-invoice";
        if (s.includes("CALL BACK") || s.includes("FOLLOW") || s.includes("RNR")) return "grad-callback";
        if (s.includes("LEAD")) return "grad-lead";
        if (s.includes("TRIAL")) return "grad-trial";
        if (s.includes("DIRECT")) return "grad-direct";
        return "grad-default";
    }

    function generateConversionsSVGString() {
        const counts = window.lastConversionsCounts || {};
        const maxCount = Math.max(...Object.values(counts), 1);
        const statuses = Object.keys(counts);
        
        let svg = `<svg width="600" height="560" viewBox="0 0 600 560" xmlns="http://www.w3.org/2000/svg" style="background-color: #ffffff; font-family: 'Inter', system-ui, -apple-system, sans-serif;">`;
        
        svg += `
        <defs>
          <linearGradient id="grad-hot" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#f97316" />
            <stop offset="100%" stop-color="#ef4444" />
          </linearGradient>
          <linearGradient id="grad-slate" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#94a3b8" />
            <stop offset="100%" stop-color="#64748b" />
          </linearGradient>
          <linearGradient id="grad-onboarded" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#10b981" />
            <stop offset="100%" stop-color="#14b8a6" />
          </linearGradient>
          <linearGradient id="grad-proposal" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#a855f7" />
            <stop offset="100%" stop-color="#6366f1" />
          </linearGradient>
          <linearGradient id="grad-demo-scheduled" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#38bdf8" />
            <stop offset="100%" stop-color="#3b82f6" />
          </linearGradient>
          <linearGradient id="grad-demo-done" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#22d3ee" />
            <stop offset="100%" stop-color="#3b82f6" />
          </linearGradient>
          <linearGradient id="grad-invoice" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#ec4899" />
            <stop offset="100%" stop-color="#f43f5e" />
          </linearGradient>
          <linearGradient id="grad-callback" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#fbbf24" />
            <stop offset="100%" stop-color="#f97316" />
          </linearGradient>
          <linearGradient id="grad-lead" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#2dd4bf" />
            <stop offset="100%" stop-color="#3b82f6" />
          </linearGradient>
          <linearGradient id="grad-trial" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#0ea5e9" />
            <stop offset="100%" stop-color="#6366f1" />
          </linearGradient>
          <linearGradient id="grad-direct" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#0d9488" />
            <stop offset="100%" stop-color="#059669" />
          </linearGradient>
          <linearGradient id="grad-default" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#14b8a6" />
            <stop offset="100%" stop-color="#1e90ff" />
          </linearGradient>
        </defs>
        `;
        
        svg += `<text x="25" y="35" font-size="16" font-weight="800" fill="#0f172a">Stage-wise Conversions</text>`;
        svg += `<text x="25" y="55" font-size="11" font-weight="500" fill="#64748b">Report Filter: ${currentStageFilter.toUpperCase()}</text>`;
        
        statuses.forEach((sName, index) => {
            const count = counts[sName] || 0;
            const pct = maxCount > 0 ? (count / maxCount) : 0;
            const barWidth = Math.round(pct * 360);
            
            const rowOffset = 80 + index * 31;
            const textY = rowOffset + 10;
            const barY = rowOffset;
            
            svg += `<text x="25" y="${textY}" font-size="11" font-weight="600" fill="#475569">${sName}</text>`;
            svg += `<rect x="160" y="${barY}" width="360" height="12" rx="6" fill="#f1f5f9" />`;
            
            if (barWidth > 0) {
                const gradId = getSVGStatusGradientId(sName);
                svg += `<rect x="160" y="${barY}" width="${barWidth}" height="12" rx="6" fill="url(#${gradId})" />`;
            }
            
            svg += `<text x="535" y="${textY}" font-size="11" font-weight="700" fill="#1e293b">${count} Leads</text>`;
        });
        
        svg += `</svg>`;
        return svg;
    }

    function downloadConversionsChart(type) {
        if (!window.lastConversionsCounts) return;
        
        if (type === 'csv') {
            const csvRows = ["Status,Count"];
            for (const [status, count] of Object.entries(window.lastConversionsCounts)) {
                csvRows.push(`"${status.replace(/"/g, '""')}",${count}`);
            }
            const csvString = csvRows.join("\n");
            const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement("a");
            const url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", "stage_wise_conversions.csv");
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);
        } else if (type === 'svg') {
            const svgString = generateConversionsSVGString();
            const blob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' });
            const link = document.createElement("a");
            const url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", "stage_wise_conversions.svg");
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);
        } else if (type === 'png') {
            const svgString = generateConversionsSVGString();
            const img = new Image();
            const svgBlob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' });
            const url = URL.createObjectURL(svgBlob);
            img.onload = function() {
                const canvas = document.createElement("canvas");
                canvas.width = 1200;
                canvas.height = 1120;
                const ctx = canvas.getContext("2d");
                ctx.scale(2, 2);
                ctx.drawImage(img, 0, 0);
                
                const pngUrl = canvas.toDataURL("image/png");
                const link = document.createElement("a");
                link.setAttribute("href", pngUrl);
                link.setAttribute("download", "stage_wise_conversions.png");
                link.style.visibility = 'hidden';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                URL.revokeObjectURL(url);
            };
            img.src = url;
        }
    }

    // Helper to get matching gradient classes for stage bars
    function getStatusGradient(statusName) {
        const s = statusName.toUpperCase();
        if (s.includes("HOT")) return "from-orange-500 to-red-500";
        if (s.includes("LOST") || s.includes("DUPLICATE")) return "from-slate-400 to-slate-500";
        if (s.includes("ONBOARDED")) return "from-emerald-500 to-teal-500";
        if (s.includes("PROPOSAL")) return "from-purple-500 to-indigo-500";
        if (s.includes("DEMO SCHEDULED") || s.includes("DEMO SCHEDULE")) return "from-sky-400 to-blue-500";
        if (s.includes("DEMO DONE") || s.includes("DEMO")) return "from-cyan-400 to-blue-500";
        if (s.includes("INVOICE")) return "from-pink-500 to-rose-500";
        if (s.includes("CALL BACK") || s.includes("FOLLOW") || s.includes("RNR")) return "from-amber-400 to-orange-500";
        if (s.includes("LEAD")) return "from-teal-400 to-blue-500";
        if (s.includes("TRIAL")) return "from-sky-500 to-indigo-500";
        if (s.includes("DIRECT")) return "from-teal-500 to-emerald-600";
        return "from-teal-500 to-[#1E90FF]"; // default
    }

    // Helper to get solid hex color for stage pie chart
    function getStatusHexColor(statusName) {
        const s = statusName.toUpperCase();
        if (s.includes("HOT")) return "#f97316";
        if (s.includes("LOST") || s.includes("DUPLICATE")) return "#64748b";
        if (s.includes("ONBOARDED")) return "#10b981";
        if (s.includes("PROPOSAL")) return "#8b5cf6";
        if (s.includes("DEMO SCHEDULED") || s.includes("DEMO SCHEDULE")) return "#0ea5e9";
        if (s.includes("DEMO DONE") || s.includes("DEMO")) return "#06b6d4";
        if (s.includes("INVOICE")) return "#ec4899";
        if (s.includes("CALL BACK") || s.includes("FOLLOW") || s.includes("RNR")) return "#fbbf24";
        if (s.includes("LEAD")) return "#14b8a6";
    }

    window.showDonutCenterInfo = function(label, pct, countStr, color) {
        const titleEl = document.getElementById('donut-center-title');
        const valEl = document.getElementById('donut-center-value');
        if (titleEl && valEl) {
            titleEl.textContent = label.toUpperCase();
            titleEl.setAttribute('fill', color);
            if (label.length > 12) {
                titleEl.setAttribute('font-size', '9');
            } else {
                titleEl.setAttribute('font-size', '11');
            }
            valEl.textContent = `${pct} (${countStr.split(' ')[0]})`;
        }
    };

    window.resetDonutCenterInfo = function(totalCount) {
        const titleEl = document.getElementById('donut-center-title');
        const valEl = document.getElementById('donut-center-value');
        if (titleEl && valEl) {
            titleEl.textContent = 'TOTAL';
            titleEl.setAttribute('fill', '#94a3b8');
            titleEl.setAttribute('font-size', '11');
            valEl.textContent = totalCount;
        }
    };

    // Load & Calculate Stats
    function loadStats() {
        let rawLeads = [];
        try {
            const stored = localStorage.getItem('leadsData');
            if (stored) rawLeads = JSON.parse(stored);
        } catch(e) {}

        const now = new Date();
        const startOfToday = new Date(now.getFullYear(), now.getMonth(), now.getDate()).getTime();

        // 1. Filter leads for Sales Funnel (and overall stats)
        const leads = rawLeads.filter(lead => {
            if (currentFilter === 'all') return true;

            let leadTime = 0;
            if (lead.date) {
                leadTime = Number(lead.date);
            } else if (lead.creationDate) {
                const parsed = Date.parse(lead.creationDate.replace(/-/g, ' '));
                if (!isNaN(parsed)) leadTime = parsed;
            }

            if (leadTime === 0) return false;

            if (currentFilter === 'today') {
                return leadTime >= startOfToday;
            } else if (currentFilter === '1week') {
                return leadTime >= (now.getTime() - 7 * 24 * 60 * 60 * 1000);
            } else if (currentFilter === '15days') {
                return leadTime >= (now.getTime() - 15 * 24 * 60 * 60 * 1000);
            } else if (currentFilter === '1month') {
                return leadTime >= (now.getTime() - 30 * 24 * 60 * 60 * 1000);
            }
            return true;
        });

        // 2. Filter leads for Stage-wise Conversions chart
        const conversionsLeads = rawLeads.filter(lead => {
            if (currentStageFilter === 'all') return true;

            let leadTime = 0;
            if (lead.date) {
                leadTime = Number(lead.date);
            } else if (lead.creationDate) {
                const parsed = Date.parse(lead.creationDate.replace(/-/g, ' '));
                if (!isNaN(parsed)) leadTime = parsed;
            }

            if (leadTime === 0) return false;

            if (currentStageFilter === 'today') {
                return leadTime >= startOfToday;
            } else if (currentStageFilter === '1week') {
                return leadTime >= (now.getTime() - 7 * 24 * 60 * 60 * 1000);
            } else if (currentStageFilter === '15days') {
                return leadTime >= (now.getTime() - 15 * 24 * 60 * 60 * 1000);
            } else if (currentStageFilter === '1month') {
                return leadTime >= (now.getTime() - 30 * 24 * 60 * 60 * 1000);
            }
            return true;
        });

        const totalLeads = leads.length;
        const activeLeads = leads.filter(l => l.stage !== 'LOST' && l.stage !== 'ONBOARDED').length;
        const convertedLeads = leads.filter(l => l.stage === 'ONBOARDED').length;
        const conversionRate = totalLeads > 0 ? Math.round((convertedLeads / totalLeads) * 100) : 0;

        document.getElementById('stat-total-leads').textContent = totalLeads;
        document.getElementById('stat-active-leads').textContent = activeLeads;
        document.getElementById('stat-converted-leads').textContent = convertedLeads;
        document.getElementById('stat-conversion-rate').textContent = `${conversionRate}%`;

        // Render Sales Funnel Stage Distribution
        const statusDisplayNames = [
            "Lead",
            "Lost",
            "Follow Up",
            "Proposal Sent",
            "Others",
            "Hot",
            "Trial Account",
            "Onboarded",
            "Demo Done",
            "RNR",
            "Call Back",
            "Invoice Sent",
            "Demo Scheduled",
            "Duplicate",
            "Direct Meeting"
        ];

        const STATUS_ALIASES = {
            "LEAD": ["LEAD"],
            "LOST": ["LOST"],
            "FOLLOW UP": ["FOLLOW UP"],
            "PROPOSAL SENT": ["PROPOSAL SENT"],
            "OTHERS": ["OTHERS"],
            "HOT": ["HOT"],
            "TRIAL ACCOUNT": ["TRIAL ACCOUNT", "TRIAL AC"],
            "ONBOARDED": ["ONBOARDED"],
            "DEMO DONE": ["DEMO DONE"],
            "RNR": ["RNR"],
            "CALL BACK": ["CALL BACK"],
            "INVOICE SENT": ["INVOICE SENT", "INVOICE"],
            "DEMO SCHEDULED": ["DEMO SCHEDULED", "DEMO SCHEDULE"],
            "DUPLICATE": ["DUPLICATE"],
            "DIRECT MEETING": ["DIRECT MEETING"]
        };

        const stageCounts = {};
        statusDisplayNames.forEach(name => {
            stageCounts[name] = 0;
        });

        leads.forEach(l => {
            const rawStage = (l.stage || '').toUpperCase().trim();
            let matched = false;
            for (const dispName of statusDisplayNames) {
                const aliases = STATUS_ALIASES[dispName.toUpperCase()] || [dispName.toUpperCase()];
                if (aliases.includes(rawStage)) {
                    stageCounts[dispName]++;
                    matched = true;
                    break;
                }
            }
            if (!matched) {
                const found = statusDisplayNames.find(n => n.toUpperCase() === rawStage);
                if (found) {
                    stageCounts[found]++;
                } else {
                    stageCounts["Others"]++;
                }
            }
        });

        const chartContainer = document.getElementById('stage-chart-container');
        chartContainer.innerHTML = '';

        const totalFunnelLeads = Object.values(stageCounts).reduce((a, b) => a + b, 0);

        const radius = 75;
        const strokeWidth = 20;
        const circumference = 2 * Math.PI * radius; // ~471.24
        
        let svgContent = `<svg width="200" height="200" viewBox="0 0 200 200" class="w-full h-full">`;
        let legendHTML = '';

        if (totalFunnelLeads === 0) {
            // Draw a single light-gray circle
            svgContent += `
                <circle cx="100" cy="100" r="${radius}" 
                        fill="transparent" 
                        stroke="#e2e8f0" 
                        stroke-width="${strokeWidth}" />
            `;
        } else {
            let cumulativeOffset = 0;
            const activeStages = statusDisplayNames
                .map(sName => ({ name: sName, count: stageCounts[sName] }))
                .filter(item => item.count > 0);

            activeStages.forEach(item => {
                const count = item.count;
                const pct = (count / totalFunnelLeads) * 100;
                const pctRounded = Math.round(pct);
                const color = getStatusHexColor(item.name);
                const segmentLength = (pct / 100) * circumference;
                
                svgContent += `
                    <circle cx="100" cy="100" r="${radius}" 
                            fill="transparent" 
                            stroke="${color}" 
                            stroke-width="${strokeWidth}" 
                            stroke-dasharray="${segmentLength} ${circumference}" 
                            stroke-dashoffset="-${cumulativeOffset}" 
                            transform="rotate(-90 100 100)"
                            onmouseover="window.showDonutCenterInfo('${item.name}', '${pctRounded}%', '${count} Leads', '${color}')"
                            onmouseout="window.resetDonutCenterInfo('${totalFunnelLeads}')"
                            class="transition-all duration-300 hover:stroke-[24] cursor-pointer" />
                `;
                cumulativeOffset += segmentLength;
            });
        }

        // Build the legend items listing all statuses in order, with square color bullets (always shown!)
        statusDisplayNames.forEach(sName => {
            const color = getStatusHexColor(sName);
            legendHTML += `
                <div class="flex items-center gap-2 text-[11px] py-0.5 select-none hover:bg-slate-100/50 dark:hover:bg-slate-800/50 rounded px-1 transition-colors">
                    <span class="w-3.5 h-3.5 rounded-sm shrink-0 border border-slate-200/10" style="background-color: ${color}"></span>
                    <span class="text-slate-650 dark:text-slate-400 font-semibold truncate" title="${sName}">${sName}</span>
                </div>
            `;
        });

        svgContent += `
            <text x="100" y="95" font-size="12" fill="#94a3b8" text-anchor="middle" font-weight="bold" class="font-sans" id="donut-center-title">TOTAL</text>
            <text x="100" y="118" font-size="20" fill="#1e293b" text-anchor="middle" font-weight="extrabold" class="font-sans dark:fill-white" id="donut-center-value">${totalFunnelLeads}</text>
        </svg>
        `;

        chartContainer.innerHTML = `
            <div class="flex flex-col md:flex-row items-center justify-center gap-8 h-full py-2 w-full">
                <div class="w-[200px] h-[200px] shrink-0 relative flex items-center justify-center">
                    ${svgContent}
                </div>
                <!-- Excel-style Legend Card -->
                <div class="bg-slate-50 dark:bg-slate-800/30 border border-slate-200/60 dark:border-slate-700/60 rounded-xl p-3 w-[170px] shrink-0 text-slate-700 dark:text-slate-350 self-start custom-scrollbar overflow-y-auto max-h-[280px] space-y-2">
                    <div class="flex items-center gap-1 text-slate-400 dark:text-slate-500 font-bold text-[9px] uppercase tracking-wider">
                        <span class="material-symbols-outlined text-[12px] rotate-90">play_arrow</span>
                        Status
                    </div>
                    <div class="space-y-1">
                        ${legendHTML}
                    </div>
                </div>
            </div>
        `;

        // Render Stage-wise Conversions Chart using alphabetical sorting
        const conversionsStatusDisplayNames = [
            "Call Back",
            "Demo Done",
            "Demo Scheduled",
            "Direct Meeting",
            "Duplicate",
            "Follow Up",
            "Hot",
            "Invoice Sent",
            "Lead",
            "Lost",
            "Onboarded",
            "Others",
            "Proposal Sent",
            "RNR",
            "Trial Account"
        ];

        const conversionsSTATUS_ALIASES = {
            "CALL BACK": ["CALL BACK"],
            "DEMO DONE": ["DEMO DONE"],
            "DEMO SCHEDULED": ["DEMO SCHEDULED", "DEMO SCHEDULE"],
            "DIRECT MEETING": ["DIRECT MEETING"],
            "DUPLICATE": ["DUPLICATE"],
            "FOLLOW UP": ["FOLLOW UP"],
            "HOT": ["HOT"],
            "INVOICE SENT": ["INVOICE SENT", "INVOICE"],
            "LEAD": ["LEAD"],
            "LOST": ["LOST"],
            "ONBOARDED": ["ONBOARDED"],
            "OTHERS": ["OTHERS"],
            "PROPOSAL SENT": ["PROPOSAL SENT"],
            "RNR": ["RNR"],
            "TRIAL ACCOUNT": ["TRIAL ACCOUNT", "TRIAL AC"]
        };

        const conversionsCounts = {};
        conversionsStatusDisplayNames.forEach(name => {
            conversionsCounts[name] = 0;
        });

        conversionsLeads.forEach(l => {
            const rawStage = (l.stage || '').toUpperCase().trim();
            let matched = false;
            for (const dispName of conversionsStatusDisplayNames) {
                const aliases = conversionsSTATUS_ALIASES[dispName.toUpperCase()] || [dispName.toUpperCase()];
                if (aliases.includes(rawStage)) {
                    conversionsCounts[dispName]++;
                    matched = true;
                    break;
                }
            }
            if (!matched) {
                const found = conversionsStatusDisplayNames.find(n => n.toUpperCase() === rawStage);
                if (found) {
                    conversionsCounts[found]++;
                } else {
                    conversionsCounts["Others"]++;
                }
            }
        });

        window.lastConversionsCounts = conversionsCounts; // Save computed counts globally for download exports

        const conversionsContainer = document.getElementById('conversions-chart-container');
        conversionsContainer.innerHTML = '';
        const maxConversionsCount = Math.max(...Object.values(conversionsCounts), 1);

        conversionsStatusDisplayNames.forEach(sName => {
            const count = conversionsCounts[sName];
            const pct = Math.round((count / maxConversionsCount) * 100);
            
            const div = document.createElement('div');
            div.className = 'space-y-1.5';
            div.innerHTML = `
                <div class="flex justify-between text-xs font-semibold text-slate-650 dark:text-slate-400">
                    <span>${sName}</span>
                    <span class="font-bold">${count} Leads</span>
                </div>
                <div class="w-full bg-slate-100 dark:bg-slate-800/80 h-3 rounded-full overflow-hidden">
                    <div class="bg-gradient-to-r ${getStatusGradient(sName)} h-full rounded-full transition-all duration-500" style="width: ${pct}%"></div>
                </div>
            `;
            conversionsContainer.appendChild(div);
        });

        // Render Source Breakdown
        // Filter leads for Source-wise Leads based on currentSourceFilter
        const sourceLeads = rawLeads.filter(lead => {
            if (currentSourceFilter === 'all') return true;

            let leadTime = 0;
            if (lead.date) {
                leadTime = Number(lead.date);
            } else if (lead.creationDate) {
                const parsed = Date.parse(lead.creationDate.replace(/-/g, ' '));
                if (!isNaN(parsed)) leadTime = parsed;
            }

            if (leadTime === 0) return false;

            if (currentSourceFilter === 'today') {
                return leadTime >= startOfToday;
            } else if (currentSourceFilter === '1week') {
                return leadTime >= (now.getTime() - 7 * 24 * 60 * 60 * 1000);
            } else if (currentSourceFilter === '15days') {
                return leadTime >= (now.getTime() - 15 * 24 * 60 * 60 * 1000);
            } else if (currentSourceFilter === '1month') {
                return leadTime >= (now.getTime() - 30 * 24 * 60 * 60 * 1000);
            }
            return true;
        });

        // Load configured sources from settings
        let configuredSources = [];
        try {
            const storedSources = localStorage.getItem('leadSourcesData');
            if (storedSources) {
                const parsed = JSON.parse(storedSources);
                if (Array.isArray(parsed)) {
                    configuredSources = parsed.map(s => (s.name || '').toUpperCase().trim()).filter(Boolean);
                }
            }
        } catch(e) {}

        const sourceCounts = {};
        // Pre-populate with all configured sources (set counts to 0)
        configuredSources.forEach(src => {
            sourceCounts[src] = 0;
        });

        // Count leads per source
        sourceLeads.forEach(l => {
            const rawSrc = (l.source || '').toUpperCase().trim();
            if (rawSrc) {
                if (sourceCounts[rawSrc] !== undefined) {
                    sourceCounts[rawSrc]++;
                } else if (configuredSources.length === 0) {
                    // Fallback: track dynamically if no configured sources exist
                    sourceCounts[rawSrc] = (sourceCounts[rawSrc] || 0) + 1;
                } else {
                    // Include any unconfigured source dynamically to prevent data loss
                    sourceCounts[rawSrc] = (sourceCounts[rawSrc] || 0) + 1;
                }
            }
        });

        const sourcesContainer = document.getElementById('sources-list-container');
        sourcesContainer.innerHTML = '';
        const sortedSources = Object.entries(sourceCounts).sort((a,b) => b[1] - a[1]);
        const totalSourceLeadsCount = Object.values(sourceCounts).reduce((a, b) => a + b, 0);

        sortedSources.forEach(([src, count]) => {
            const srcPct = totalSourceLeadsCount > 0 ? Math.round((count / totalSourceLeadsCount) * 100) : 0;
            const div = document.createElement('div');
            div.className = 'flex items-center justify-between text-xs';
            div.innerHTML = `
                <div class="flex items-center gap-2">
                    <span class="material-symbols-outlined text-[#0D9488] text-[16px]">campaign</span>
                    <span class="font-semibold text-slate-700 dark:text-slate-300 truncate max-w-[150px]">${src}</span>
                </div>
                <div class="flex items-center gap-3">
                    <span class="text-slate-400 dark:text-slate-500">${srcPct}%</span>
                    <span class="font-bold text-slate-700 dark:text-slate-300 w-8 text-right">${count}</span>
                </div>
            `;
            sourcesContainer.appendChild(div);
        });
        if (sortedSources.length === 0) {
            sourcesContainer.innerHTML = `<div class="text-slate-400 text-xs py-4 text-center">No sources configured yet</div>`;
        }

        // Render Recent Leads
        const recentLeadsTbody = document.getElementById('recent-leads-tbody');
        recentLeadsTbody.innerHTML = '';
        
        const recent = leads.slice(-5).reverse();
        recent.forEach(lead => {
            const tr = document.createElement('tr');
            tr.className = 'hover:bg-slate-50/50 dark:hover:bg-slate-800/30 transition-colors';
            tr.innerHTML = `
                <td class="py-3 font-bold text-slate-800 dark:text-slate-200">${lead.name}</td>
                <td class="py-3"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-teal-50 dark:bg-teal-950/20 text-[#0D9488] dark:text-teal-400 border border-teal-150 dark:border-teal-900/50">${lead.stage}</span></td>
                <td class="py-3 text-slate-700 dark:text-slate-300">${lead.mobile || '-'}</td>
                <td class="py-3 text-slate-500 dark:text-slate-400">${lead.source || '-'}</td>
                <td class="py-3 text-slate-500 dark:text-slate-400">${lead.user || '-'}</td>
                <td class="py-3 text-slate-400 dark:text-slate-500 text-[11px]">${lead.creationDate || '-'}</td>
            `;
            recentLeadsTbody.appendChild(tr);
        });
        if (recent.length === 0) {
            recentLeadsTbody.innerHTML = `<tr><td colspan="6" class="py-8 text-center text-slate-400 dark:text-slate-500 text-xs">No leads loaded</td></tr>`;
        }
    }

    document.addEventListener('DOMContentLoaded', () => {
        initClock();
        initDarkMode();
        loadStats();
    });

    // Injected Change Password Dropdown Logic
    function toggleChangePasswordMenu(event) {
        event.stopPropagation();
        const menu = document.getElementById('change-password-menu');
        const adminMenu = document.getElementById('admin-menu');
        if (adminMenu) adminMenu.classList.add('hidden');
        document.querySelectorAll('.dropdown-menu').forEach(m => {
            if (m.id !== 'change-password-menu') m.classList.add('hidden');
        });
        if (menu) menu.classList.toggle('hidden');
    }

    function handleHeaderChangePassword(event) {
        event.preventDefault();
        const form = event.target;
        const oldPass = form.querySelector('.header-old-pass').value;
        const newPass = form.querySelector('.header-new-pass').value;
        const confirmPass = form.querySelector('.header-confirm-pass').value;

        const session = JSON.parse(localStorage.getItem('crmActiveSession') || 'null');
        if (!session) {
            showToast('No active session found.', 'error');
            return;
        }

        let users = [];
        try { users = JSON.parse(localStorage.getItem('crmUsers') || '[]'); } catch(e) {}
        
        const userIdx = users.findIndex(u => u.username.toLowerCase() === session.username.toLowerCase());
        if (userIdx === -1) {
            showToast('User not found.', 'error');
            return;
        }

        if (oldPass !== users[userIdx].password) {
            showToast('Incorrect old password!', 'error');
            return;
        }

        if (newPass.length < 6) {
            showToast('New password must be at least 6 characters!', 'error');
            return;
        }

        if (newPass !== confirmPass) {
            showToast('New password and confirm password do not match!', 'error');
            return;
        }

        if (newPass === oldPass) {
            showToast('New password cannot be the same as old password!', 'error');
            return;
        }

        users[userIdx].password = newPass;
        localStorage.setItem('crmUsers', JSON.stringify(users));

        showToast('Password updated successfully!');
        form.reset();
        
        const menu = document.getElementById('change-password-menu');
        if (menu) menu.classList.add('hidden');

        if (typeof verifySession === 'function') {
            verifySession();
        }
    }

    if (typeof showForgotPasswordModal !== 'function') {
        window.showForgotPasswordModal = function() {
            const session = JSON.parse(localStorage.getItem('crmActiveSession') || 'null');
            if (!session) return;
            let users = [];
            try { users = JSON.parse(localStorage.getItem('crmUsers') || '[]'); } catch(e) {}
            const user = users.find(u => u.username.toLowerCase() === session.username.toLowerCase());
            if (user) {
                const modal = document.getElementById('forgot-password-modal');
                if (modal) {
                    document.getElementById('retrieved-password').textContent = user.password;
                    document.getElementById('retrieved-email').textContent = user.email || 'your registered email';
                    modal.classList.remove('hidden');
                } else {
                    alert('For sandbox testing, your current password is: ' + user.password);
                }
            }
        };
    }

    function toggleAdminMenu(event) {
        event.stopPropagation();
        const menu = document.getElementById('admin-menu');
        const cpMenu = document.getElementById('change-password-menu');
        if (cpMenu) cpMenu.classList.add('hidden');
        if (menu) menu.classList.toggle('hidden');
    }

    if (typeof showToast !== 'function') {
        window.showToast = function(message, type = 'success') {
            let container = document.getElementById('toast-container');
            if (!container) {
                container = document.createElement('div');
                container.id = 'toast-container';
                container.className = 'fixed top-4 right-4 z-50 flex flex-col gap-3';
                document.body.appendChild(container);
            }

            const toast = document.createElement('div');
            toast.className = 'flex items-center gap-2 px-4 py-3 rounded-xl shadow-lg border text-xs font-bold transition-all duration-300 transform translate-x-12 opacity-0';
            
            let icon = 'check_circle';
            if (type === 'success') {
                toast.className += ' bg-emerald-50 border-emerald-250 text-emerald-700';
            } else if (type === 'error') {
                toast.className += ' bg-red-50 border-red-250 text-red-750';
                icon = 'error';
            } else {
                toast.className += ' bg-slate-50 border-slate-250 text-slate-700';
                icon = 'info';
            }

            toast.innerHTML = `<span class="material-symbols-outlined text-[18px]">${icon}</span><span>${message}</span>`;
            container.appendChild(toast);
            
            setTimeout(() => {
                toast.classList.remove('translate-x-12', 'opacity-0');
            }, 10);

            setTimeout(() => {
                toast.classList.add('translate-x-12', 'opacity-0');
                setTimeout(() => toast.remove(), 300);
            }, 3000);
        };
    }

    document.addEventListener('click', () => {
        const cpMenu = document.getElementById('change-password-menu');
        if (cpMenu) cpMenu.classList.add('hidden');
    });


    // Injected Login Activity Dropdown Logic
    function toggleLoginActivityMenu(event) {
        event.stopPropagation();
        const menu = document.getElementById('login-activity-menu');
        const adminMenu = document.getElementById('admin-menu');
        if (adminMenu) adminMenu.classList.add('hidden');
        document.querySelectorAll('.dropdown-menu').forEach(m => {
            if (m.id !== 'login-activity-menu') m.classList.add('hidden');
        });
        if (menu) {
            menu.classList.toggle('hidden');
            if (!menu.classList.contains('hidden')) {
                renderHeaderLoginLogs();
            }
        }
    }

    function renderHeaderLoginLogs() {
        const tbodies = document.querySelectorAll('.header-login-activity-tbody');
        if (tbodies.length === 0) return;

        const session = JSON.parse(localStorage.getItem('crmActiveSession') || 'null');
        if (!session) return;

        let logs = [];
        try {
            logs = JSON.parse(localStorage.getItem('crmLoginActivities') || '[]');
        } catch(e) {}

        logs = logs.filter(a => a.username.toLowerCase() === session.username.toLowerCase());

        if (logs.length === 0) {
            logs = seedMockLoginLogsHeader(session.username);
        }

        const recent = logs.slice().reverse().slice(0, 5);

        tbodies.forEach(tbody => {
            tbody.innerHTML = '';
            recent.forEach((log, index) => {
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-50/50 transition-colors';
                
                const loginStr = formatHeaderDateTime(new Date(log.loginAt));
                const logoutStr = log.logoutAt ? formatHeaderDateTime(new Date(log.logoutAt)) : '<span class="text-emerald-600 font-bold">Active</span>';
                const durationStr = log.logoutAt ? log.duration : '--';
                const serialNo = logs.length - index;

                tr.innerHTML = `
                    <td class="py-1.5 px-2 font-semibold text-slate-500">${serialNo}</td>
                    <td class="py-1.5 px-2 font-medium text-slate-700">${loginStr}</td>
                    <td class="py-1.5 px-2 font-medium text-slate-750">${logoutStr}</td>
                    <td class="py-1.5 px-2 font-bold text-slate-650">${durationStr}</td>
                    <td class="py-1.5 px-2 font-mono text-slate-500">${log.ip}</td>
                `;
                tbody.appendChild(tr);
            });

            if (recent.length === 0) {
                tbody.innerHTML = '<tr><td colspan="5" class="py-4 text-center text-slate-400 text-xs">No records.</td></tr>';
            }
        });
    }

    function formatHeaderDateTime(date) {
        const dd = String(date.getDate()).padStart(2, '0');
        const mm = String(date.getMonth() + 1).padStart(2, '0');
        const yyyy = date.getFullYear();
        const hh = String(date.getHours()).padStart(2, '0');
        const min = String(date.getMinutes()).padStart(2, '0');
        return `${dd}-${mm} ${hh}:${min}`;
    }

    function seedMockLoginLogsHeader(username) {
        const logs = [];
        const ips = ['192.168.1.102', '192.168.1.15', '172.16.4.52', '10.0.0.15', '192.168.1.200', '198.51.100.24', '203.0.113.88'];
        const now = Date.now();

        for (let i = 15; i >= 1; i--) {
            const loginOffset = i * 8 * 60 * 60 * 1000;
            const loginTime = now - loginOffset;
            const durationMin = Math.floor(Math.random() * 120) + 15;
            const logoutTime = i === 1 ? null : loginTime + (durationMin * 60 * 1000);
            
            let durationStr = '--';
            if (logoutTime) {
                const hours = Math.floor(durationMin / 60);
                const mins = durationMin % 60;
                durationStr = hours > 0 ? `${hours}h ${mins}m` : `${mins}m`;
            }

            logs.push({
                username: username,
                serial: 16 - i,
                loginAt: loginTime,
                logoutAt: logoutTime,
                duration: durationStr,
                ip: ips[Math.floor(Math.random() * ips.length)]
            });
        }

        let allLogs = [];
        try { allLogs = JSON.parse(localStorage.getItem('crmLoginActivities') || '[]'); } catch(e) {}
        allLogs = allLogs.filter(a => a.username.toLowerCase() !== username.toLowerCase());
        allLogs = [...allLogs, ...logs];
        localStorage.setItem('crmLoginActivities', JSON.stringify(allLogs));

        return logs;
    }

    window.toggleAdminMenu = function(event) {
        event.stopPropagation();
        const menu = document.getElementById('admin-menu');
        const laMenu = document.getElementById('login-activity-menu');
        if (laMenu) laMenu.classList.add('hidden');
        if (menu) menu.classList.toggle('hidden');
    };

    document.addEventListener('click', () => {
        const laMenu = document.getElementById('login-activity-menu');
        if (laMenu) laMenu.classList.add('hidden');
    });



