$ErrorActionPreference = "Stop"

try {
    Write-Host "Initializing Word COM Object..."
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0

    $docPath = "c:\dulieulon\Kich_Ban_Thuyet_Trinh_Bao_Ve_BTL.docx"
    $pdfPath = "c:\dulieulon\Kich_Ban_Thuyet_Trinh_Bao_Ve_BTL.pdf"

    Write-Host "Opening document: $docPath"
    $doc = $word.Documents.Open($docPath, $false, $true)

    $pages = $doc.ComputeStatistics(2)
    Write-Host "Total Document Pages: $pages"

    Write-Host "Exporting to PDF: $pdfPath"
    $wdFormatPDF = 17
    $doc.SaveAs([ref]$pdfPath, [ref]$wdFormatPDF)

    $doc.Close([ref]$false)
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()

    Write-Host "SUCCESS: Exported $pdfPath successfully ($pages pages)"
} catch {
    Write-Host "Error: $($_.Exception.Message)"
    if ($word) {
        try { $word.Quit() } catch {}
    }
}
