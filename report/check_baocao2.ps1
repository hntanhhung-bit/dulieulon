$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open('c:\dulieulon\BaoCao 2.docx', $false, $true)
    $pages = $doc.ComputeStatistics(2)
    Write-Host "Total Pages in BaoCao 2.docx: $pages"
    
    # Export to PDF as well
    $pdfPath = "c:\dulieulon\BaoCao 2.pdf"
    $wdFormatPDF = 17
    $doc.SaveAs([ref]$pdfPath, [ref]$wdFormatPDF)
    Write-Host "Exported PDF to: $pdfPath"
    $doc.Close([ref]$false)
} finally {
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
}
