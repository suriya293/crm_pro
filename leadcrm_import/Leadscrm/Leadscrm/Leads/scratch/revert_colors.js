const fs = require('fs');
const path = require('path');

const dir = path.join(__dirname, '..');
const files = fs.readdirSync(dir);

const oldStr = 'bg-[#0D9488] text-white rounded-xl font-bold shadow-md shadow-teal-950/20';
const newStr = 'bg-[#1E90FF] text-white rounded-xl font-bold shadow-md shadow-blue-900/20';

const loginActivityOldPagination = 'bg-[#0D9488] border-[#0D9488] text-white shadow-sm shadow-teal-500/10';
const loginActivityNewPagination = 'bg-[#1E90FF] border-[#1E90FF] text-white shadow-sm shadow-blue-500/10';

files.forEach(file => {
    if (file.endsWith('.html')) {
        const filePath = path.join(dir, file);
        let content = fs.readFileSync(filePath, 'utf8');
        let modified = false;
        
        if (content.includes(oldStr)) {
            content = content.split(oldStr).join(newStr);
            modified = true;
        }

        if (file === 'login_activity.html' && content.includes(loginActivityOldPagination)) {
            content = content.split(loginActivityOldPagination).join(loginActivityNewPagination);
            modified = true;
        }

        if (modified) {
            fs.writeFileSync(filePath, content, 'utf8');
            console.log(`Reverted active sidebar color in ${file}`);
        }
    }
});

console.log('Sidebar color revert complete.');
