$cp = (Get-Volume -FileSystemLabel "CIRCUITPY").DriveLetter
if (-not $cp) { exit }

$dump  = Join-Path "${cp}:" "wifi_dump.txt"
$state = Join-Path "${cp}:" "state.txt"
$out   = "$env:USERPROFILE\Desktop\WiFi_Credentials.txt"

$lines = @()

if (Test-Path $dump) {
    $lines = Get-Content $dump
}

# Build clean output explicitly
$outputText = @()
$outputText += "WiFi Credentials Extracted"
$outputText += "=========================="
$outputText += ""

if ($lines.Count -gt 0) {
    $outputText += $lines
} else {
    $outputText += "No WiFi credentials found."
}

# Write cleanly with proper line breaks
$outputText | Set-Content -Encoding ASCII $out

# Cleanup
if (Test-Path $dump) {
    Clear-Content $dump
}

Set-Content -Encoding ASCII $state "IDLE"
