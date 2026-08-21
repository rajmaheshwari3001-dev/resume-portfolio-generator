# Edit README.md (Teeya)
Add-Content -Path README.md -Value ""
Add-Content -Path README.md -Value "## Team Contributors"
Add-Content -Path README.md -Value "- Teeya"
git add README.md
git commit --author="teeya831-cmd <237906070+teeya831-cmd@users.noreply.github.com>" -m "Docs: Add Contributors section to README"

# Edit script.js (Parth)
$scriptContent = Get-Content script.js -Raw
$scriptContent = $scriptContent -replace 'async function doGenerate\(\) {', "// Handles the core API request and updates the UI state during generation`r`nasync function doGenerate() {"
Set-Content -Path script.js -Value $scriptContent -NoNewline
git add script.js
git commit --author="ParthSachdeva26 <215622443+ParthSachdeva26@users.noreply.github.com>" -m "Refactor: Add documentation to frontend API generation logic"

# Edit main.py (Shivangi)
$mainContent = Get-Content main.py -Raw
$mainContent = $mainContent -replace 'html_code = html_code.replace\("\{\{name\}\}", name\)', "# Dynamically inject the extracted JSON data into the HTML template placeholders`r`n    html_code = html_code.replace(""{{name}}"", name)"
Set-Content -Path main.py -Value $mainContent -NoNewline
git add main.py
git commit --author="ShivangiGautam08 <310996566+ShivangiGautam08@users.noreply.github.com>" -m "Refactor: Add documentation to backend HTML templating engine"

# Edit api/index.py (Bulbul)
$apiContent = Get-Content api\index.py -Raw
$apiContent = $apiContent -replace '@app.post\("/api/generate"\)', "# Main API endpoint for Vercel serverless deployment`r`n@app.post(""/api/generate"")"
Set-Content -Path api\index.py -Value $apiContent -NoNewline
git add api\index.py
git commit --author="Bulbul Ali <229190379+bulbulali22-cell@users.noreply.github.com>" -m "Docs: Comment FastAPI serverless route configuration"

# Add all other names to README (Since teeya added the header)
Add-Content -Path README.md -Value "- Parth Sachdeva"
Add-Content -Path README.md -Value "- Shivangi Gautam"
Add-Content -Path README.md -Value "- Bulbul Ali"
Add-Content -Path README.md -Value "- Raj Maheshwari"
git add README.md
git commit -m "Docs: Finalize team member list in README"

git push
