try {
    $ppt = New-Object -ComObject PowerPoint.Application
    Write-Host "PowerPoint Version: $($ppt.Version)"
    $ppt.Quit()
} catch {
    Write-Host "PowerPoint Error: $($_.Exception.Message)"
}
