$content = Get-Content 'listview.html' -Raw

# Replace title
$content = $content -replace '<title>Leads - List View</title>', '<title>Leads</title>'

# Replace the view toggle block (lines 215-229)
# We match it using regular expressions, escaping properly or matching unique tags
$pattern = '(?s)\s*<!-- View Toggle \(back to Grid\) -->.*?</div>\s*</div>'
# Let's inspect the target pattern first or match it specifically:
# From "<!-- View Toggle" to the matching closing tag of `<div class="relative">`.
$target = @"
            <!-- View Toggle (back to Grid) -->
            <div class="relative">
                <button onclick="toggleDropdown(event, 'view-dropdown')" class="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-[#0D9488] to-[#0ea5e9] hover:from-[#0F766E] hover:to-[#0284c7] text-white border-none rounded-full text-xs font-bold transition-all shadow-sm">
                    <span>List View</span>
                    <span class="material-symbols-outlined text-[14px]">expand_more</span>
                </button>
                <div id="view-dropdown" class="absolute left-0 mt-1.5 w-36 bg-white border border-slate-100 rounded-xl shadow-lg py-1 z-20 hidden dropdown-menu">
                    <a href="code.html" class="w-full text-left px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors flex items-center justify-between">
                        Grid View <span class="material-symbols-outlined text-[16px] text-slate-300">open_in_new</span>
                    </a>
                    <button class="w-full text-left px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors flex items-center justify-between">
                        List View <span class="material-symbols-outlined text-[16px] text-teal-600">check</span>
                    </button>
                </div>
            </div>
"@

$content = $content.Replace($target, "")

Set-Content 'code.html' -Value $content -Encoding utf8
Write-Output "Copied listview.html to code.html with grid view toggle removed."
