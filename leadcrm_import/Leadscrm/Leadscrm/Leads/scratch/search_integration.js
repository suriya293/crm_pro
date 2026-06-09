const fs = require('fs');
const path = require('path');

const files = fs.readdirSync('.').filter(f => f.endsWith('.html') || f.endsWith('.js'));

files.forEach(filepath => {
    try {
        const content = fs.readFileSync(filepath, 'utf8');
        const fbMatches = content.match(/facebook|fb_/gi) || [];
        const waMatches = content.match(/whatsapp|wa_/gi) || [];
        if (fbMatches.length > 0 || waMatches.length > 0) {
            console.log(`${filepath}: ${fbMatches.length} FB, ${waMatches.length} WA`);
            const lines = content.split('\n');
            lines.forEach((line, i) => {
                const lower = line.toLowerCase();
                if (lower.includes('facebook') || lower.includes('fb_') || lower.includes('whatsapp') || lower.includes('wa_')) {
                    console.log(`  Line ${i+1}: ${line.trim().slice(0, 120)}`);
                }
            });
        }
    } catch (e) {
        console.error(`Error reading ${filepath}:`, e);
    }
});
