$ErrorActionPreference = "Stop"

try {
    Write-Host "Initializing PowerPoint COM Object..."
    $ppt = New-Object -ComObject PowerPoint.Application

    $pptxPath = "c:\dulieulon\Slide.pptx"
    $pdfPath = "c:\dulieulon\Slide.pdf"

    Write-Host "Opening presentation: $pptxPath"
    # Parameters: FileName, ReadOnly (0), Untitled (0), WithWindow (0)
    $pres = $ppt.Presentations.Open($pptxPath, 0, 0, 0)
    Write-Host "Slides count: $($pres.Slides.Count)"

    Write-Host "Exporting to PDF: $pdfPath"
    # ppSaveAsPDF = 32
    $pres.SaveAs($pdfPath, 32)

    $pres.Close()
    $ppt.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($ppt) | Out-Null
    [System.GC]::Collect()

    if (Test-Path $pdfPath) {
        $pdfItem = Get-Item $pdfPath
        Write-Host "SUCCESS: Slide.pdf created successfully!"
        Write-Host "File Size: $($pdfItem.Length) bytes"
    } else {
        Write-Error "Slide.pdf not found after export."
    }
} catch {
    Write-Host "Error occurred: $($_.Exception.Message)"
    if ($ppt) {
        $ppt.Quit()
    }
    exit 1
}
