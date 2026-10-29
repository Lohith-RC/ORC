
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open("C:\Users\Rakshith YB\ORC-3\docs\test_num.docx")
    $doc.SaveAs([ref]"C:\Users\Rakshith YB\ORC-3\docs\test_num.pdf", [ref]17)
    $doc.Close([ref]0)
} finally {
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}
