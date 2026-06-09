const fs = require('fs');
const path = require('path');
const vm = require('vm');

const dir = path.join(__dirname, '..');
const files = fs.readdirSync(dir);

files.forEach(file => {
    if (file.endsWith('.html')) {
        const filePath = path.join(dir, file);
        const content = fs.readFileSync(filePath, 'utf8');

        // Match everything between <script> and </script>
        const scriptRegex = /<script[^>]*>([\s\S]*?)<\/script>/gi;
        let match;
        let count = 0;

        while ((match = scriptRegex.exec(content)) !== null) {
            const code = match[1];
            if (code.trim().length === 0) continue;
            count++;
            try {
                new vm.Script(code);
            } catch (e) {
                console.error(`Syntax error in file ${file}, script block ${count}:`, e);
                process.exit(1);
            }
        }
        console.log(`Validated ${file}: ${count} script blocks are syntax-valid.`);
    }
});

console.log('All HTML files script blocks are syntax-valid.');
