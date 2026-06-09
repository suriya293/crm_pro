$files = @("c:\Users\YUVEHA\OneDrive\Documents\Leads\listview.html")

foreach ($file in $files) {
    if (Test-Path $file) {
        $content = [System.IO.File]::ReadAllText($file)

        # Remove the complex tailwind config
        $content = $content -replace 'tailwind\.config\s*=\s*\{[\s\S]*?\}\s*</script>', 'tailwind.config = { darkMode: "class" }</script>'
        
        # Replace heavy dark/blue colors with normal ones
        $content = $content -replace 'bg-\[#1E3A8A\]', 'bg-blue-600'
        $content = $content -replace 'bg-\[#2563eb\]', 'bg-blue-600'
        $content = $content -replace 'text-\[#1E3A8A\]', 'text-blue-600'
        $content = $content -replace 'border-\[#1E3A8A\]', 'border-blue-600'
        $content = $content -replace 'text-\[#2563eb\]', 'text-blue-600'
        
        $content = $content -replace 'bg-\[#F3F4F6\]', 'bg-slate-50'
        $content = $content -replace 'text-\[#0F172A\]', 'text-slate-800'
        $content = $content -replace 'bg-\[#ECFDF5\]', 'bg-emerald-50'
        $content = $content -replace 'text-\[#0F766E\]', 'text-emerald-700'
        
        # Replace pink hover state
        $content = $content -replace 'hover:bg-\[#EC4899\]', 'hover:bg-slate-100'
        $content = $content -replace 'hover:text-\[#EC4899\]', 'hover:text-blue-600'
        $content = $content -replace 'hover:shadow-\[#EC4899\]', 'hover:shadow-slate-300'
        
        # Fix sidebar gradient
        $content = $content -replace 'bg-gradient-to-b from-primary to-tertiary', 'bg-white border-r border-slate-200'
        $content = $content -replace 'bg-gradient-to-r from-primary to-tertiary', 'bg-blue-600 hover:bg-blue-700'
        
        # Fix dark mode html tag
        $content = $content -replace '<html class="light"', '<html'
        $content = $content -replace '<html class="dark"', '<html'

        [System.IO.File]::WriteAllText($file, $content)
        Write-Output "Processed $file"
    }
}
