$docxPath = "C:\Users\lohit\OneDrive\Desktop\Oral Canser Detection (1)\ORC\docs\vtu_final_report.docx"
$pdfPath  = "C:\Users\lohit\OneDrive\Desktop\Oral Canser Detection (1)\ORC\docs\vtu_final_report.pdf"

Write-Host "Opening Microsoft Word Application..."
$word = New-Object -ComObject Word.Application
$word.Visible = $false

try {
    Write-Host "Opening Document: $docxPath"
    $doc = $word.Documents.Open($docxPath)
    Write-Host "Exporting to PDF: $pdfPath"
    # 17 = wdFormatPDF
    $doc.SaveAs([ref]$pdfPath, [ref]17)
    $doc.Close([ref]0) # 0 = wdDoNotSaveChanges
    Write-Host "PDF export finished successfully!"
}
catch {
    Write-Error $_.Exception.Message
}
finally {
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
}
