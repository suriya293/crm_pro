import re

html_code = open('view_lead.html', encoding='utf-8').read()

activities_ui = """                        <!-- Activities Tab -->
                        <div id="tab-content-activities" class="hidden space-y-8">
                            
                            <!-- Notes Section -->
                            <div>
                                <div class="flex justify-between items-center mb-4">
                                    <h3 class="text-base font-black text-slate-800">1. Notes</h3>
                                    <button onclick="document.getElementById('modal-add-note').classList.remove('hidden')" class="px-3 py-1.5 bg-[#0D9488] text-white text-xs font-bold rounded-lg hover:bg-[#0F766E] shadow-sm flex items-center gap-1">
                                        <span class="material-symbols-outlined text-[16px]">add</span> Add Note
                                    </button>
                                </div>
                                <div class="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm text-sm">
                                    <div class="overflow-x-auto custom-scrollbar">
                                        <table class="w-full text-left border-collapse">
                                            <thead>
                                                <tr class="bg-slate-50 text-slate-500 text-[10px] uppercase tracking-wider font-bold border-b border-slate-100">
                                                    <th class="px-4 py-3 whitespace-nowrap">Sr. No.</th>
                                                    <th class="px-4 py-3 whitespace-nowrap">Created Date</th>
                                                    <th class="px-4 py-3 whitespace-nowrap">User</th>
                                                    <th class="px-4 py-3 whitespace-nowrap">Note</th>
                                                    <th class="px-4 py-3 whitespace-nowrap">Uploaded File</th>
                                                    <th class="px-4 py-3 whitespace-nowrap">Action</th>
                                                </tr>
                                            </thead>
                                            <tbody class="text-slate-700">
                                                <tr class="border-b border-slate-50 hover:bg-slate-50/50 transition-colors">
                                                    <td class="px-4 py-3 font-bold">1</td>
                                                    <td class="px-4 py-3">10-06-2026</td>
                                                    <td class="px-4 py-3 font-semibold">Admin</td>
                                                    <td class="px-4 py-3">Followed up with customer</td>
                                                    <td class="px-4 py-3"><a href="#" class="text-blue-600 hover:underline flex items-center gap-1 text-xs"><span class="material-symbols-outlined text-[14px]">description</span> document.pdf</a></td>
                                                    <td class="px-4 py-3">
                                                        <div class="flex gap-2">
                                                            <button class="text-blue-600 hover:text-blue-800 text-xs font-bold transition-colors">View</button>
                                                            <span class="text-slate-300">|</span>
                                                            <button class="text-red-500 hover:text-red-700 text-xs font-bold transition-colors">Delete</button>
                                                        </div>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>

                            <hr class="border-slate-200">

                            <!-- Tasks Section -->
                            <div>
                                <div class="flex justify-between items-center mb-4">
                                    <h3 class="text-base font-black text-slate-800">2. Tasks</h3>
                                    <button onclick="document.getElementById('modal-add-task').classList.remove('hidden')" class="px-3 py-1.5 bg-[#0D9488] text-white text-xs font-bold rounded-lg hover:bg-[#0F766E] shadow-sm flex items-center gap-1">
                                        <span class="material-symbols-outlined text-[16px]">add</span> Add Task
                                    </button>
                                </div>
                                
                                <!-- Task Filters -->
                                <div class="flex items-center gap-2 mb-4 overflow-x-auto custom-scrollbar pb-1">
                                    <button class="px-4 py-1.5 rounded-full text-xs font-bold bg-slate-800 text-white transition-colors">All</button>
                                    <button class="px-4 py-1.5 rounded-full text-xs font-bold bg-slate-100 text-slate-600 hover:bg-slate-200 transition-colors">Open</button>
                                    <button class="px-4 py-1.5 rounded-full text-xs font-bold bg-slate-100 text-slate-600 hover:bg-slate-200 transition-colors">Overdue</button>
                                    <button class="px-4 py-1.5 rounded-full text-xs font-bold bg-slate-100 text-slate-600 hover:bg-slate-200 transition-colors">Completed</button>
                                </div>

                                <div class="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm text-sm">
                                    <div class="overflow-x-auto custom-scrollbar">
                                        <table class="w-full text-left border-collapse">
                                            <thead>
                                                <tr class="bg-slate-50 text-slate-500 text-[10px] uppercase tracking-wider font-bold border-b border-slate-100">
                                                    <th class="px-4 py-3 whitespace-nowrap">Sr. No.</th>
                                                    <th class="px-4 py-3 whitespace-nowrap">Date</th>
                                                    <th class="px-4 py-3 whitespace-nowrap">Task Name</th>
                                                    <th class="px-4 py-3 whitespace-nowrap">Description</th>
                                                    <th class="px-4 py-3 whitespace-nowrap">Assigned To</th>
                                                    <th class="px-4 py-3 whitespace-nowrap">Status</th>
                                                    <th class="px-4 py-3 whitespace-nowrap">Type</th>
                                                    <th class="px-4 py-3 whitespace-nowrap">Outcome</th>
                                                    <th class="px-4 py-3 whitespace-nowrap">Action</th>
                                                </tr>
                                            </thead>
                                            <tbody class="text-slate-700">
                                                <tr class="border-b border-slate-50 hover:bg-slate-50/50 transition-colors">
                                                    <td class="px-4 py-3 font-bold">1</td>
                                                    <td class="px-4 py-3">10-06-2026</td>
                                                    <td class="px-4 py-3 font-bold text-slate-800">Follow-up Call</td>
                                                    <td class="px-4 py-3 max-w-[200px] truncate" title="Contact lead regarding quotation">Contact lead regarding quotation</td>
                                                    <td class="px-4 py-3 font-semibold">John</td>
                                                    <td class="px-4 py-3"><span class="px-2 py-0.5 rounded bg-amber-50 text-amber-600 border border-amber-100 text-[10px] uppercase font-bold">Open</span></td>
                                                    <td class="px-4 py-3">Call</td>
                                                    <td class="px-4 py-3">Pending</td>
                                                    <td class="px-4 py-3">
                                                        <div class="flex gap-2 items-center">
                                                            <button class="text-[#0D9488] hover:text-[#0F766E] text-xs font-bold transition-colors">Edit</button>
                                                            <span class="text-slate-300">|</span>
                                                            <button class="text-red-500 hover:text-red-700 text-xs font-bold transition-colors">Delete</button>
                                                            <span class="text-slate-300">|</span>
                                                            <button class="text-emerald-600 hover:text-emerald-800 text-[16px] transition-colors" title="Mark as Completed"><span class="material-symbols-outlined">check_circle</span></button>
                                                        </div>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        </div>"""

modals_ui = """
<!-- Add Note Modal -->
<div id="modal-add-note" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 hidden">
    <div class="bg-white rounded-2xl shadow-xl w-full max-w-md overflow-hidden animate-[fadeIn_0.2s_ease-out]">
        <div class="flex items-center justify-between px-6 py-4 border-b border-slate-100 bg-slate-50/50">
            <h3 class="text-lg font-black text-slate-800">Add Note</h3>
            <button onclick="document.getElementById('modal-add-note').classList.add('hidden')" class="text-slate-400 hover:text-slate-600 transition-colors">
                <span class="material-symbols-outlined">close</span>
            </button>
        </div>
        <div class="p-6 space-y-4">
            <div>
                <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1">Note Details</label>
                <textarea rows="4" class="w-full px-3 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-teal-500 focus:border-teal-500 text-sm transition-all" placeholder="Enter your note here..."></textarea>
            </div>
            <div>
                <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1">Upload File <span class="text-[10px] text-slate-400 normal-case font-normal">(Optional)</span></label>
                <input type="file" accept=".pdf,.csv,.xlsx,.jpg,.jpeg,.png" class="w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-bold file:bg-teal-50 file:text-teal-700 hover:file:bg-teal-100 transition-all"/>
                <p class="text-[10px] text-slate-400 mt-1">Supported: PDF, CSV, Excel, JPG, PNG</p>
            </div>
        </div>
        <div class="flex items-center justify-end gap-3 px-6 py-4 bg-slate-50 border-t border-slate-100">
            <button onclick="document.getElementById('modal-add-note').classList.add('hidden')" class="px-4 py-2 text-sm font-bold text-slate-600 hover:bg-slate-200 bg-slate-100 rounded-xl transition-colors">Cancel</button>
            <button onclick="document.getElementById('modal-add-note').classList.add('hidden')" class="px-5 py-2 text-sm font-bold text-white bg-[#0D9488] hover:bg-[#0F766E] rounded-xl shadow-sm transition-colors">Save Note</button>
        </div>
    </div>
</div>

<!-- Add Task Modal -->
<div id="modal-add-task" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 hidden">
    <div class="bg-white rounded-2xl shadow-xl w-full max-w-lg overflow-hidden animate-[fadeIn_0.2s_ease-out]">
        <div class="flex items-center justify-between px-6 py-4 border-b border-slate-100 bg-slate-50/50">
            <h3 class="text-lg font-black text-slate-800">Add Task</h3>
            <button onclick="document.getElementById('modal-add-task').classList.add('hidden')" class="text-slate-400 hover:text-slate-600 transition-colors">
                <span class="material-symbols-outlined">close</span>
            </button>
        </div>
        <div class="p-6 space-y-4 max-h-[70vh] overflow-y-auto custom-scrollbar">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="md:col-span-2">
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1">Task Name</label>
                    <input type="text" class="w-full px-3 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-teal-500 text-sm transition-all" placeholder="E.g., Follow-up Call"/>
                </div>
                <div class="md:col-span-2">
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1">Description</label>
                    <textarea rows="2" class="w-full px-3 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-teal-500 text-sm transition-all" placeholder="Enter task details..."></textarea>
                </div>
                <div>
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1">Assigned To</label>
                    <select class="w-full px-3 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-teal-500 text-sm transition-all">
                        <option>Admin</option>
                        <option>John Doe</option>
                    </select>
                </div>
                <div>
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1">Due Date</label>
                    <input type="date" class="w-full px-3 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-teal-500 text-sm transition-all"/>
                </div>
                <div>
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1">Status</label>
                    <select class="w-full px-3 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-teal-500 text-sm transition-all">
                        <option>Open</option>
                        <option>Completed</option>
                        <option>Overdue</option>
                    </select>
                </div>
                <div>
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1">Type</label>
                    <select class="w-full px-3 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-teal-500 text-sm transition-all">
                        <option>Call</option>
                        <option>Email</option>
                        <option>Meeting</option>
                        <option>Other</option>
                    </select>
                </div>
                <div class="md:col-span-2">
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1">Outcome</label>
                    <input type="text" class="w-full px-3 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-teal-500 text-sm transition-all" placeholder="E.g., Pending, Spoke to client..."/>
                </div>
            </div>
        </div>
        <div class="flex items-center justify-end gap-3 px-6 py-4 bg-slate-50 border-t border-slate-100">
            <button onclick="document.getElementById('modal-add-task').classList.add('hidden')" class="px-4 py-2 text-sm font-bold text-slate-600 hover:bg-slate-200 bg-slate-100 rounded-xl transition-colors">Cancel</button>
            <button onclick="document.getElementById('modal-add-task').classList.add('hidden')" class="px-5 py-2 text-sm font-bold text-white bg-[#0D9488] hover:bg-[#0F766E] rounded-xl shadow-sm transition-colors">Save Task</button>
        </div>
    </div>
</div>
"""

# Replace old activities tab with new one
old_activities_regex = r'<div id="tab-content-activities" class="hidden space-y-4">.*?</div>\s*<!-- Timeline Tab -->'
html_code = re.sub(old_activities_regex, activities_ui + '\n\n                        <!-- Timeline Tab -->', html_code, flags=re.DOTALL)

# Inject modals before script tag
html_code = html_code.replace('<script>', modals_ui + '\n<script>')

with open('view_lead.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

print("Injected activities module into view_lead.html successfully!")
