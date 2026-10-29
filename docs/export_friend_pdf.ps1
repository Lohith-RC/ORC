
$docxPath = "C:\Users\Rakshith YB\ORC-3\docs\Career_Navigator_IRJMETS.docx"
$pdfPath  = "C:\Users\Rakshith YB\ORC-3\docs\Career_Navigator_IRJMETS.pdf"

$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open($docxPath)
    $doc.SaveAs([ref]$pdfPath, [ref]17)
    $doc.Close([ref]0)
    Write-Host "Friend PDF Export Succeeded!"
} catch {
    Write-Error $_.Exception.Message
    exit 1
} finally {
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}
