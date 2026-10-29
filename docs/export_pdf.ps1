
$docxPath = "C:\Users\Rakshith YB\ORC-3\docs\ORAL_CANCER_IRJMETS_MANUSCRIPT.docx"
$pdfPath  = "C:\Users\Rakshith YB\ORC-3\docs\ORAL_CANCER_IRJMETS_MANUSCRIPT.pdf"

Write-Host "Starting Word Application..."
$word = New-Object -ComObject Word.Application
$word.Visible = $false

try {
    Write-Host "Opening Document: $docxPath"
    $doc = $word.Documents.Open($docxPath)
    Write-Host "Exporting to PDF: $pdfPath"
    # 17 = wdFormatPDF
    $doc.SaveAs([ref]$pdfPath, [ref]17)
    $doc.Close([ref]0)
    Write-Host "PDF Export Succeeded!"
}
catch {
    Write-Error $_.Exception.Message
    exit 1
}
finally {
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
}
