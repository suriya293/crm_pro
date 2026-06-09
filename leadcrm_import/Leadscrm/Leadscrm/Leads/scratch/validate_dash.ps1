$content = Get-Content 'dashboard.html' -Raw
if ($content -match '(?s)<script>(.*?)</script>') {
    Set-Content 'scratch/test_dash.js' $matches[1]
    node -c scratch/test_dash.js
} else {
    Write-Output "No script block found"
}
