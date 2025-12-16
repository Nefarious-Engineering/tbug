$cp = (Get-Volume -FileSystemLabel "CIRCUITPY").DriveLetter
if (-not $cp) { exit }

$state = Join-Path "${cp}:" "state.txt"
Set-Content -Encoding ASCII $state "IDLE"