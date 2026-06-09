"# apply_theme_headers.ps1

$dir = "c:\Users\YUVEHA\OneDrive\Documents\Leads"
$files = @("listview.html", "settings.html", "user.html", "group.html", "stage.html", "channel.html")

$darkModeCss = @"
    <style>
        /* Premium Slate/Midnight Dark Mode Aesthetics */
        html.dark body {
            background-color: #0f172a !important;
            color: #cbd5e1 !important;
        }
        html.dark .bg-white {
            background-color: #1e293b !important;
            color: #f8fafc !important;
        }
        html.dark .bg-slate-50\/50, html.dark .bg-slate-50 {
            background-color: #1e293b !important;
        }
        html.dark .text-slate-700 {
            color: #cbd5e1 !important;
        }
        html.dark .text-slate-600 {
            color: #94a3b8 !important;
        }
        html.dark .text-slate-550, html.dark .text-slate-500 {
            color: #94a3b8 !important;
        }
        html.dark .text-slate-800 {
            color: #f1f5f9 !important;
        }
        html.dark .border-slate-200, html.dark .border-slate-100, html.dark .border-slate-50 {
            border-color: #334155 !important;
        }
        html.dark header, html.dark .bg-white.border-b {
            background-color: #0f172a !important;
            border-color: #334155 !important;
        }
        html.dark select, html.dark input, html.dark textarea {
            background-color: #1e293b !important;
            color: #cbd5e1 !important;
            border-color: #334155 !important;
        }
        html.dark .hover\:bg-slate-50:hover, html.dark .hover\:bg-slate-100:hover {
            background-color: #334155 !important;
        }
        html.dark .text-slate-400 {
            color: #64748b !important;
        }
        html.dark .bg-[#F3F4F6], html.dark .bg-[#f8fafc], html.dark .bg-[#f4f6f8] {
            background-color: #0f172a !important;
        }
        html.dark table th {
            background-color: #1e293b
<truncated 14074 bytes>