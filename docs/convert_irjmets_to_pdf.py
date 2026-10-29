import subprocess
import os
import sys

docx_path = os.path.abspath("docs/ORAL_CANCER_IRJMETS_MANUSCRIPT.docx")
pdf_path = os.path.abspath("docs/ORAL_CANCER_IRJMETS_MANUSCRIPT.pdf")

print(f"Converting DOCX: {docx_path}")
print(f"Target PDF:   {pdf_path}")

ps_code = f"""
$docxPath = "{docx_path}"
$pdfPath  = "{pdf_path}"

Write-Host "Starting Word Application..."
$word = New-Object -ComObject Word.Application
$word.Visible = $false

try {{
    Write-Host "Opening Document: $docxPath"
    $doc = $word.Documents.Open($docxPath)
    Write-Host "Exporting to PDF: $pdfPath"
    # 17 = wdFormatPDF
    $doc.SaveAs([ref]$pdfPath, [ref]17)
    $doc.Close([ref]0)
    Write-Host "PDF Export Succeeded!"
}}
catch {{
    Write-Error $_.Exception.Message
    exit 1
}}
finally {{
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
}}
"""

ps_script_path = os.path.abspath("docs/export_pdf.ps1")
with open(ps_script_path, "w", encoding="utf-8") as f:
    f.write(ps_code)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_script_path], capture_output=True, text=True)
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)

if os.path.exists(pdf_path):
    print(f"SUCCESS: PDF generated! Size: {os.path.getsize(pdf_path)} bytes")
else:
    print("FAILED: PDF not found.")
    sys.exit(1)
