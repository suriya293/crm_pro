const fs = require('fs');
const path = require('path');

const dir = path.join(__dirname, '..');
const files = fs.readdirSync(dir);

const oldStr = 'bg-[#1E90FF] text-white rounded-xl font-bold shadow-md shadow-blue-900/20';
const newStr = 'bg-[#0D9488] text-white rounded-xl font-bold shadow-md shadow-teal-950/20';

files.forEach(file => {
    if (file.endsWith('.html')) {
        const filePath = path.join(dir, file);
        let content = fs.readFileSync(filePath, 'utf8');
        if (content.includes(oldStr)) {
            content = content.split(oldStr).join(newStr);
            fs.writeFileSync(filePath, content, 'utf8');
            console.log(`Updated active sidebar color in ${file}`);
        }
    }
});

console.log('Sidebar color replacement complete.');
