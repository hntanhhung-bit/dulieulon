$ErrorActionPreference = "Stop"

try {
    Write-Host "Creating Word COM object..."
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0

    $docPath = "c:\dulieulon\BaoCao.docx"
    $pdfPath = "c:\dulieulon\BaoCao.pdf"

    Write-Host "Opening document..."
    $doc = $word.Documents.Open($docPath, $false, $true)

    Write-Host "Testing ExportAsFixedFormat..."
    # wdExportFormatPDF = 17
    # wdExportOptimizeForPrint = 0
    # wdExportAllDocument = 0
    $doc.ExportAsFixedFormat($pdfPath, 17, $false, 0, 0, 1, 1, 0, $true, $true, 1, $true, $true, $false)

    Write-Host "Closing document..."
    try { $doc.Close([ref]$false) } catch {}
    try { $word.Quit() } catch {}
    try { [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null } catch {}
    [System.GC]::Collect()

    if (Test-Path $pdfPath) {
        $pdfFile = Get-Item $pdfPath
        Write-Host "SUCCESS: BaoCao.pdf exported successfully!"
        Write-Host "PDF Size: $($pdfFile.Length) bytes"
        Write-Host "Last Modified: $($pdfFile.LastWriteTime)"
    } else {
        Write-Host "PDF not found."
    }
} catch {
    Write-Host "Export error: $($_.Exception.Message)"
    try { if ($word) { $word.Quit() } } catch {}
}
