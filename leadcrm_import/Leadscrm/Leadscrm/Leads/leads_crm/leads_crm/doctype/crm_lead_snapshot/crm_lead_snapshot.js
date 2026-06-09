# Copyright (c) 2026, Administrator and contributors
# For license information, please see license.txt

frappe.ui.form.on('CRM Lead Snapshot', {
	refresh: function(frm) {
		// Provide simple form cues if needed
	},
	total_leads: function(frm) {
		calculate_conversion_rate(frm);
	},
	converted_leads: function(frm) {
		calculate_conversion_rate(frm);
	}
});

function calculate_conversion_rate(frm) {
	if (frm.doc.total_leads > 0) {
		let rate = (frm.doc.converted_leads / frm.doc.total_leads) * 100;
		frm.set_value('conversion_rate', parseFloat(rate.toFixed(2)));
	} else {
		frm.set_value('conversion_rate', 0.0);
	}
}
