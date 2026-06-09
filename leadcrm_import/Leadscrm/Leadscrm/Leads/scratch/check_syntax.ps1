$content = Get-Content 'dashboard.html' -Raw
$matches = [regex]::Matches($content, '(?s)<script.*?>(.*?)</script>')
$scriptBlock = ""
foreach ($m in $matches) {
    $scriptBlock += $m.Groups[1].Value + "`n"
}
if (!(Test-Path 'scratch')) {
    New-Item -ItemType Directory -Path 'scratch' | Out-Null
}
Set-Content 'scratch/test_dashboard_syntax.js' $scriptBlock
node -c scratch/test_dashboard_syntax.js
