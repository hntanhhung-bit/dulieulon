$ErrorActionPreference = "Stop"

try {
    Write-Host "Initializing Word Application COM Object..."
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0 # 0 = wdAlertsNone

    $docPath = "c:\dulieulon\BaoCao.docx"
    $pdfPath = "c:\dulieulon\BaoCao.pdf"

    Write-Host "Opening document: $docPath"
    $doc = $word.Documents.Open($docPath, $false, $true)

    # Compute page count (2 = wdStatisticPages)
    $pages = $doc.ComputeStatistics(2)
    Write-Host "=========================================="
    Write-Host "Total Document Pages in Microsoft Word: $pages"
    Write-Host "=========================================="

    # Export to PDF (17 = wdFormatPDF)
    Write-Host "Exporting to PDF: $pdfPath"
    $wdFormatPDF = 17
    $doc.SaveAs([ref]$pdfPath, [ref]$wdFormatPDF)

    # Close document without saving changes (0 = wdDoNotSaveChanges)
    $doc.Close([ref]$false)
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()

    if (Test-Path $pdfPath) {
        $pdfFile = Get-Item $pdfPath
        Write-Host "SUCCESS: PDF created successfully!"
        Write-Host "File Name: $($pdfFile.Name)"
        Write-Host "File Size: $($pdfFile.Length) bytes"
    } else {
        Write-Error "PDF file was not found after export."
    }
} catch {
    Write-Host "Error occurred: $($_.Exception.Message)"
    if ($word) {
        $word.Quit()
    }
    exit 1
}
